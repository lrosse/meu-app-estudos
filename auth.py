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
        # Se quiser ver o erro no console do Streamlit, descomente a linha abaixo:
        # st.error(f"Erro no login: {e}")
        return False

def registrar_usuario(usuario, senha):
    try:
        # 1. Tenta ler os dados atuais
        try:
            df = conn.read(worksheet="Usuarios", ttl=0)
            # Se a aba existe mas está vazia de dados (só cabeçalho ou nada)
            if df is None or df.empty:
                df = pd.DataFrame(columns=["usuario", "senha"])
        except Exception:
            # Se a aba nem sequer existir
            df = pd.DataFrame(columns=["usuario", "senha"])

        # 2. Garante que as colunas existem antes de verificar
        if "usuario" not in df.columns:
            df = pd.DataFrame(columns=["usuario", "senha"])

        # 3. Verifica se o usuário já existe
        if usuario in df["usuario"].astype(str).values:
            st.warning("Este nome de usuário já está em uso.")
            return False
        
        # 4. Cria o novo registro
        novo_user = pd.DataFrame([{"usuario": str(usuario), "senha": str(senha)}])
        
        # 5. Junta com os dados antigos (garantindo que não venha lixo)
        df_atualizado = pd.concat([df, novo_user], ignore_index=True).dropna(how='all')
        
        # 6. ENVIO CRÍTICO: Tenta atualizar a planilha
        conn.update(worksheet="Usuarios", data=df_atualizado)
        
        # Limpa o cache para garantir que a próxima leitura veja o novo usuário
        st.cache_data.clear()
        return True
    except Exception as e:
        # Isso vai mostrar o erro real na tela para você me dizer o que é:
        st.error(f"Erro técnico ao registrar: {e}")
        return False
