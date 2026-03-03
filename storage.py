import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Inicializa a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    """Lê os dados da planilha do Google"""
    try:
        # Tenta ler a aba 'Estudos'. Se não existir, retorna lista vazia
        df = conn.read(worksheet="Estudos", ttl=0) # ttl=0 garante dados em tempo real
        if df.empty:
            return []
        
        # Converte o DataFrame de volta para a lista de dicionários (formato do seu app)
        import json
        dados = df.to_dict(orient="records")
        
        # Ajuste: A coluna 'revisoes' volta de String para Lista
        for item in dados:
            if isinstance(item["revisoes"], str):
                item["revisoes"] = json.loads(item["revisoes"].replace("'", '"'))
        return dados
    except Exception:
        return []

def save_data(dados):
    """Salva a lista completa na planilha do Google"""
    import json
    
    # Prepara os dados para o formato de tabela (Flatten)
    df_para_salvar = pd.DataFrame(dados)
    
    # Transforma a lista de revisões em texto para caber na célula do Excel
    df_para_salvar["revisoes"] = df_para_salvar["revisoes"].apply(lambda x: json.dumps(x))
    
    # Sobrescreve a aba 'Estudos' com os novos dados
    conn.update(worksheet="Estudos", data=df_para_salvar)
    st.cache_data.clear() # Limpa o cache para mostrar a mudança na hora