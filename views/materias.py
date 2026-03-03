import streamlit as st
import pandas as pd
from storage import load_data

def calcular_taxa_geral(topico):
    """Soma questões e acertos do diagnóstico + todas as revisões já feitas."""
    total_questoes = topico["diag_questoes"]
    total_acertos = topico["diag_acertos"]
    
    for rev in topico["revisoes"]:
        if rev["feita"]:
            total_questoes += rev["meta_questoes"]
            total_acertos += rev["acertos"]
            
    if total_questoes == 0:
        return 0.0
    return round((total_acertos / total_questoes) * 100, 2)

def renderizar():
    st.header("📚 Visualização por Matéria")
    
    dados = load_data()
    if not dados:
        st.info("Nenhum dado encontrado.")
        return
        
    materias_unicas = sorted(list(set([item["materia"] for item in dados])))
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        materia_selecionada = st.selectbox("Selecione a Matéria:", materias_unicas)
        
    topicos_materia = [item for item in dados if item["materia"] == materia_selecionada]
    
    with col2:
        st.metric(label="Quantidade de Tópicos", value=len(topicos_materia))
        
    st.subheader(f"Tópicos de {materia_selecionada}")
    
    # Gerando os dados (Mantendo a taxa como número real)
    df_filtrado = pd.DataFrame([{
        "Tópico": t["topico"], 
        "Taxa Geral (Progresso)": calcular_taxa_geral(t), 
        "Prevalência": t["prevalencia"]
    } for t in topicos_materia])
    
    # --- ESTILIZAÇÃO ---
    def colorir_zebra(row):
        return ['background-color: #1e1e27' if row.name % 2 == 0 else 'background-color: #2b2b36' for _ in row]

    # Aplicando zebra, formatação de % e a barra de progresso verde
    df_estilizado = df_filtrado.style.apply(colorir_zebra, axis=1)
    df_estilizado = df_estilizado.format({"Taxa Geral (Progresso)": "{:.1f}%"})
    df_estilizado = df_estilizado.bar(subset=["Taxa Geral (Progresso)"], color='#2ea043', vmin=0, vmax=100)
    
    st.dataframe(df_estilizado, use_container_width=True, hide_index=True)