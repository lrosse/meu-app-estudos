import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json

# ---------------------------------------------------------------------------
# Conexão única, reutilizada por todas as funções
# ---------------------------------------------------------------------------
conn = st.connection("gsheets", type=GSheetsConnection)

# Nome fixo da aba de dados — altere aqui se precisar mudar
WORKSHEET = "Topicos"


def _usuario_logado() -> str:
    """Retorna o nome do usuário da sessão atual.
    Lança um erro claro se for chamado sem sessão ativa (nunca deve ocorrer
    em produção, mas ajuda muito no debug).
    """
    usuario = st.session_state.get("usuario_logado", "").strip()
    if not usuario:
        raise RuntimeError(
            "Nenhum usuário logado na sessão. "
            "Certifique-se de que st.session_state.usuario_logado está definido antes de chamar storage."
        )
    return usuario


def _ler_planilha_bruta() -> pd.DataFrame:
    """Lê TODOS os registros da planilha (todas as linhas, todos os usuários).
    Uso interno — as funções públicas sempre filtram por usuário depois.
    """
    try:
        df = conn.read(worksheet=WORKSHEET, ttl=0)
        # Garante que a coluna obrigatória existe mesmo numa planilha nova/vazia
        if df.empty or "usuario" not in df.columns:
            return pd.DataFrame()
        return df
    except Exception:
        return pd.DataFrame()


def _deserializar_revisoes(dados: list) -> list:
    """Converte a coluna 'revisoes' de string JSON para lista de dicts."""
    for item in dados:
        revisoes_raw = item.get("revisoes", "[]")
        if isinstance(revisoes_raw, str):
            try:
                item["revisoes"] = json.loads(revisoes_raw)
            except json.JSONDecodeError:
                # Fallback para o formato antigo com aspas simples (dados legados)
                item["revisoes"] = json.loads(revisoes_raw.replace("'", '"'))
    return dados


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def load_data() -> list:
    """Carrega somente os tópicos do usuário logado."""
    usuario = _usuario_logado()
    df_todos = _ler_planilha_bruta()

    if df_todos.empty:
        return []

    # Filtro de isolamento: retorna apenas as linhas do usuário atual
    df_usuario = df_todos[df_todos["usuario"].astype(str).str.strip() == usuario].copy()

    if df_usuario.empty:
        return []

    dados = df_usuario.to_dict(orient="records")
    return _deserializar_revisoes(dados)


def save_data(dados: list) -> None:
    """Salva a lista de tópicos do usuário logado, preservando dados de outros usuários.

    Estratégia:
      1. Lê a planilha inteira.
      2. Remove apenas as linhas do usuário atual.
      3. Serializa os novos dados (com a coluna `usuario` preenchida).
      4. Concatena outros usuários + novos dados do usuário atual.
      5. Sobrescreve a planilha.
    """
    usuario = _usuario_logado()

    # --- 1. Lê todos os dados existentes ---
    df_todos = _ler_planilha_bruta()

    # --- 2. Separa os dados dos OUTROS usuários (que não devem ser tocados) ---
    if not df_todos.empty and "usuario" in df_todos.columns:
        df_outros = df_todos[df_todos["usuario"].astype(str).str.strip() != usuario].copy()
    else:
        df_outros = pd.DataFrame()

    # --- 3. Prepara os dados do usuário atual para salvar ---
    if not dados:
        # Se a lista estiver vazia, o usuário apagou tudo — preserva apenas os outros
        df_final = df_outros
    else:
        df_usuario_novo = pd.DataFrame(dados)

        # Serializa revisões (lista → string JSON) para caber na célula
        df_usuario_novo["revisoes"] = df_usuario_novo["revisoes"].apply(
            lambda x: json.dumps(x, ensure_ascii=False)
        )

        # Garante que a coluna de isolamento está correta em TODOS os registros
        df_usuario_novo["usuario"] = usuario

        # --- 4. Junta os outros usuários com os dados atualizados do usuário logado ---
        if not df_outros.empty:
            # Alinha colunas para evitar NaN no concat (colunas podem diferir entre usuários)
            df_final = pd.concat([df_outros, df_usuario_novo], ignore_index=True)
        else:
            df_final = df_usuario_novo

    # --- 5. Persiste na planilha ---
    conn.update(worksheet=WORKSHEET, data=df_final)

    # Invalida o cache para que a próxima leitura seja sempre em tempo real
    st.cache_data.clear()
