import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Inicializa a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

def verificar_login(usuario, senha):
    try:
        # Tenta ler a aba Usuarios, garantindo que não use cache
        df = conn.read(worksheet="Usuarios", ttl=0)
        
        # Se a planilha estiver totalmente vazia ou sem as colunas esperadas
        if df.empty or "usuario" not in df.columns or "senha" not in df.columns:
            st.warning("Planilha de usuários vazia ou colunas ausentes.")
            return False
            
        # Limpa espaços em branco e converte para string para comparação robusta
        usuario_limpo = str(usuario).strip()
        senha_limpa = str(senha).strip()

        # Aplica .strip() e garante que as colunas são strings antes de comparar
        df["usuario_planilha"] = df["usuario"].astype(str).str.strip()
        df["senha_planilha"] = df["senha"].astype(str).str.strip()

        # --- DEBUG ATIVO ---
        st.write(f"DEBUG: Usuário input: '{usuario_limpo}', Tipo: {type(usuario_limpo)}")
        st.write(f"DEBUG: Senha input: '{senha_limpa}', Tipo: {type(senha_limpa)}")
        st.write(f"DEBUG: Usuários na planilha: {df['usuario_planilha'].tolist()}")
        st.write(f"DEBUG: Senhas na planilha: {df['senha_planilha'].tolist()}")
        # --- FIM DEBUG ATIVO ---

        # Filtra o usuário e senha usando os valores limpos
        user_row = df[(df["usuario_planilha"] == usuario_limpo) & 
                      (df["senha_planilha"] == senha_limpa)]
        
        return not user_row.empty
    except Exception as e:
        st.error(f"Erro no login: {e}")
        return False

def registrar_usuario(usuario, senha):
    try:
        # 1. Tenta ler os dados atuais para verificar se o usuário já existe
        # Usamos ttl=0 para garantir que estamos lendo os dados mais recentes
        try:
            existing_users_df = conn.read(worksheet="Usuarios", ttl=0)
        except Exception:
            # Se a aba não existir ou houver erro na leitura, criamos um DF vazio
            existing_users_df = pd.DataFrame(columns=["usuario", "senha"])

        # Garante que as colunas existem para evitar erros se a planilha estiver vazia
        if existing_users_df is None or existing_users_df.empty or "usuario" not in existing_users_df.columns:
            existing_users_df = pd.DataFrame(columns=["usuario", "senha"])

        # Limpa espaços em branco do nome de usuário antes de verificar a existência
        usuario_limpo = str(usuario).strip()

        # 2. Verifica se o usuário já existe
        # Aplica .strip() na coluna 'usuario' do DataFrame antes de verificar
        if usuario_limpo in existing_users_df["usuario"].astype(str).str.strip().values:
            st.warning("Este nome de usuário já está em uso!")
            return False
        
        # 3. Cria o novo registro
        # Armazenamos o usuário e senha limpos para evitar problemas futuros
        novo_user_df = pd.DataFrame([{"usuario": usuario_limpo, "senha": str(senha).strip()}])
        
        # 4. Concatena e atualiza a planilha inteira
        df_atualizado = pd.concat([existing_users_df, novo_user_df], ignore_index=True)
        
        conn.update(worksheet="Usuarios", data=df_atualizado)
        
        st.success("Usuário registrado com sucesso!")
        
        # Limpa o cache para garantir que a próxima leitura veja o novo usuário
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro técnico ao registrar: {e}")
        return False
