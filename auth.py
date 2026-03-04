import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Conexão única compartilhada
conn = st.connection("gsheets", type=GSheetsConnection)


def _normalizar_senha(valor: str) -> str:
    """Corrige o problema do Google Sheets que converte '1234' em '1234.0'."""
    s = str(valor).strip()
    if s.endswith(".0") and s[:-2].isdigit():
        return s[:-2]
    return s


def verificar_login(usuario: str, senha: str) -> bool:
    """Verifica credenciais contra a aba 'Usuarios' do Google Sheets.

    Retorna True se o par (usuario, senha) for encontrado, False caso contrário.
    NÃO define session_state aqui — isso é responsabilidade do app.py,
    que chama esta função e, em caso de sucesso, seta st.session_state.usuario_logado.
    """
    try:
        df = conn.read(worksheet="Usuarios", ttl=0)

        if df.empty or "usuario" not in df.columns or "senha" not in df.columns:
            st.warning("Planilha de usuários vazia ou com estrutura incorreta.")
            return False

        usuario_limpo = str(usuario).strip()
        senha_limpa = _normalizar_senha(senha)

        df["_u"] = df["usuario"].astype(str).str.strip()
        df["_s"] = df["senha"].apply(_normalizar_senha)

        encontrado = df[(df["_u"] == usuario_limpo) & (df["_s"] == senha_limpa)]
        return not encontrado.empty

    except Exception as e:
        st.error(f"Erro ao verificar login: {e}")
        return False


def registrar_usuario(usuario: str, senha: str) -> bool:
    """Cria um novo usuário na aba 'Usuarios'.

    Retorna True em caso de sucesso, False se o usuário já existir ou ocorrer erro.
    """
    try:
        # Lê registros atuais com ttl=0 para garantir consistência
        try:
            df_existentes = conn.read(worksheet="Usuarios", ttl=0)
        except Exception:
            df_existentes = pd.DataFrame(columns=["usuario", "senha"])

        if df_existentes is None or df_existentes.empty or "usuario" not in df_existentes.columns:
            df_existentes = pd.DataFrame(columns=["usuario", "senha"])

        usuario_limpo = str(usuario).strip()

        # Verifica duplicidade
        usuarios_existentes = df_existentes["usuario"].astype(str).str.strip().values
        if usuario_limpo in usuarios_existentes:
            return False  # Usuário já existe — app.py exibe a mensagem

        # Cria e persiste o novo registro
        novo = pd.DataFrame([{"usuario": usuario_limpo, "senha": str(senha).strip()}])
        df_atualizado = pd.concat([df_existentes, novo], ignore_index=True)
        conn.update(worksheet="Usuarios", data=df_atualizado)

        st.cache_data.clear()
        return True

    except Exception as e:
        st.error(f"Erro técnico ao registrar usuário: {e}")
        return False
