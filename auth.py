import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Inicializa a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

def verificar_login(usuario, senha):
    try:
        # Tenta ler a aba Usuarios
        df = conn.read(worksheet="Usuarios", ttl=0)
        
        # Se a planilha estiver totalmente vazia, o df pode vir sem as colunas
        if df.empty or "usuario" not in df.columns:
            return False
            
        # Filtra o usuário e senha
        user_row = df[(df["usuario"].astype(str) == str(usuario)) & 
                      (df["senha"].astype(str) == str(senha))]
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

        # 2. Verifica se o usuário já existe
        if usuario in existing_users_df["usuario"].astype(str).values:
            st.warning("Este nome de usuário já está em uso.")
            return False
        
        # 3. Cria o novo registro
        novo_user_df = pd.DataFrame([{"usuario": str(usuario), "senha": str(senha)}])
        
        # 4. Concatena e atualiza a planilha inteira
        # Como a biblioteca st-gsheets-connection não possui o método .append(),
        # a forma correta de adicionar dados é via .update() com o DataFrame completo.
        df_atualizado = pd.concat([existing_users_df, novo_user_df], ignore_index=True)
        
        conn.update(worksheet="Usuarios", data=df_atualizado)
        
        st.success("Usuário registrado com sucesso!")
        
        # Limpa o cache para garantir que a próxima leitura veja o novo usuário
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro técnico ao registrar: {e}")
        return False
