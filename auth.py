import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

conn = st.connection("gsheets", type=GSheetsConnection)

def verificar_login(usuario, senha):
    try:
        df = conn.read(worksheet="Usuarios", ttl=0)
        user_row = df[(df["usuario"] == usuario) & (df["senha"] == str(senha))]
        return not user_row.empty
    except:
        return False

def registrar_usuario(usuario, senha):
    try:
        # Tenta ler usuários existentes
        try:
            df = conn.read(worksheet="Usuarios", ttl=0)
        except:
            df = pd.DataFrame(columns=["usuario", "senha"])

        if usuario in df["usuario"].values:
            return False
        
        novo_user = pd.DataFrame([{"usuario": usuario, "senha": str(senha)}])
        df_atualizado = pd.concat([df, novo_user], ignore_index=True)
        
        conn.update(worksheet="Usuarios", data=df_atualizado)
        return True
    except:
        return False