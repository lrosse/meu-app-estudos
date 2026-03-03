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
        existing_users_df = conn.read(worksheet="Usuarios", ttl=0)

        # Garante que as colunas existem para evitar erros se a planilha estiver vazia
        if existing_users_df.empty or "usuario" not in existing_users_df.columns:
            existing_users_df = pd.DataFrame(columns=["usuario", "senha"])

        # 2. Verifica se o usuário já existe
        if usuario in existing_users_df["usuario"].astype(str).values:
            st.warning("Este nome de usuário já está em uso.")
            return False
        
        # 3. Cria o novo registro como um DataFrame de uma única linha
        novo_user_df = pd.DataFrame([{"usuario": str(usuario), "senha": str(senha)}])
        
        # 4. Adiciona a nova linha à planilha usando conn.append()
        # Este método é mais eficiente para adicionar novas linhas do que reescrever a planilha inteira
        conn.append(worksheet="Usuarios", data=novo_user_df)
        
        st.success("Usuário registrado com sucesso!")
        
        # Limpa o cache para garantir que a próxima leitura veja o novo usuário
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro técnico ao registrar: {e}")
        return False
