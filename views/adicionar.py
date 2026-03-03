import streamlit as st
from storage import load_data, save_data
from scheduler import calcular_taxa, gerar_revisoes
from models import criar_topico
import datetime

def hex_to_rgba(hex_color, opacity=0.25):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {opacity})'

def renderizar():
    st.header("➕ Adicionar Novo Tópico")
    
    dados = load_data()
    materias_existentes = sorted(list(set([item["materia"] for item in dados])))
    
    with st.form("form_adicionar", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            materia_existente = st.selectbox("Escolher matéria existente", ["Nova Matéria..."] + materias_existentes)
            materia_nova = st.text_input("Ou digite uma Nova Matéria:")
            materia = materia_nova if materia_existente == "Nova Matéria..." and materia_nova else materia_existente
            
            nome_topico = st.text_input("Nome do Tópico")
            data_teoria = st.date_input("Data da Teoria")
            # NOVO: O Exame pode ser até final do ano por padrão
            data_exame = st.date_input("Data da Prova/Exame (Alvo)", value=datetime.date(2026, 12, 31))
            cor_hex = st.color_picker("Cor da Matéria", "#3b82f6")
            
        with col2:
            prevalencia = st.selectbox("Prevalência", ["Alta", "Média", "Baixa"])
            questoes_diag = st.number_input("Nº questões diagnóstico", min_value=0, step=1)
            acertos_diag = st.number_input("Acertos diagnóstico", min_value=0, step=1)
            
        submit = st.form_submit_button("Salvar Tópico")
        
        if submit:
            if acertos_diag > questoes_diag:
                st.error("Acertos não podem ser maiores que as questões!")
            elif data_exame <= data_teoria:
                st.error("A data da prova precisa ser DEPOIS da data da teoria!")
            elif not materia or not nome_topico:
                st.error("Matéria e Nome são obrigatórios!")
            else:
                taxa = calcular_taxa(acertos_diag, questoes_diag)
                data_teoria_str = data_teoria.strftime("%Y-%m-%d")
                data_exame_str = data_exame.strftime("%Y-%m-%d") # Salva o texto
                
                # O gerar revisões agora calcula projetando para o futuro
                revisoes = gerar_revisoes(data_teoria_str, data_exame_str, taxa, prevalencia)
                cor_escolhida = hex_to_rgba(cor_hex)
                
                novo_topico = criar_topico(
                    materia=materia, topico=nome_topico, data_teoria=data_teoria_str, 
                    data_exame=data_exame_str, prevalencia=prevalencia, questoes_diag=questoes_diag, 
                    acertos_diag=acertos_diag, taxa_diag=taxa, revisoes=revisoes, cor_materia=cor_escolhida
                )
                
                dados.append(novo_topico)
                save_data(dados)
                st.success(f"Tópico '{nome_topico}' adicionado! Cronograma gerado inteligentemente. 🎉")