import streamlit as st
import pandas as pd
from storage import load_data
from scheduler import calcular_proxima_revisao, verificar_status
from datetime import datetime
import io  # Necessário para a exportação

# --- CALLBACK DOS FILTROS (Agora limpa a matéria também!) ---
def limpar_filtros():
    st.session_state.filtro_tipo = "Data da Teoria"
    st.session_state.filtro_abrangencia = "Mostrar Tudo"
    st.session_state.filtro_materia = "Todas as Matérias"

def renderizar():
    st.header("📋 Tabela Completa de Estudos")
    
    dados = load_data()
    if not dados:
        st.info("Nenhum tópico adicionado ainda.")
        return
        
    # --- GARANTIA DA MEMÓRIA DOS FILTROS ---
    if 'filtro_tipo' not in st.session_state:
        st.session_state.filtro_tipo = "Data da Teoria"
    if 'filtro_abrangencia' not in st.session_state:
        st.session_state.filtro_abrangencia = "Mostrar Tudo"
    if 'filtro_materia' not in st.session_state:
        st.session_state.filtro_materia = "Todas as Matérias"

    # Puxa dinamicamente todas as matérias cadastradas para o menu não ficar vazio
    materias_existentes = sorted(list(set([item["materia"] for item in dados])))
    opcoes_materia = ["Todas as Matérias"] + materias_existentes

    # --- SISTEMA DE FILTROS ---
    with st.expander("🔎 Filtros de Busca", expanded=False):
        col1, col2, col3, col4, col5 = st.columns([2.5, 2.5, 2.5, 2.5, 2])
        
        with col1:
            materia_escolhida = st.selectbox(
                "Filtrar por Matéria:", 
                opcoes_materia, 
                key="filtro_materia"
            )
            
        with col2:
            tipo_data = st.selectbox(
                "Qual data filtrar?", 
                ["Data da Teoria", "Próxima Revisão"], 
                key="filtro_tipo"
            )
            
        with col3:
            abrangencia = st.selectbox(
                "Período:", 
                ["Mostrar Tudo", "Dia Específico", "Mês Inteiro", "Ano Inteiro"], 
                key="filtro_abrangencia"
            )
            
        with col4:
            if abrangencia != "Mostrar Tudo":
                data_escolhida = st.date_input("Data base:")
            else:
                data_escolhida = None
                
        with col5:
            st.write("") 
            st.write("") 
            st.button("🧹 Limpar", on_click=limpar_filtros, use_container_width=True)

    linhas = []
    for item in dados:
        prox_data, prox_nome = calcular_proxima_revisao(item["revisoes"])
        
        # --- LÓGICA DE FILTRAGEM MULTIPLA ---
        incluir = True
        
        # 1. Passou no filtro de Matéria?
        if materia_escolhida != "Todas as Matérias" and item["materia"] != materia_escolhida:
            incluir = False
        
        # 2. Se passou na matéria, testa se passou no filtro de Data!
        if incluir and abrangencia != "Mostrar Tudo" and data_escolhida:
            data_alvo_str = item["data_teoria"] if tipo_data == "Data da Teoria" else prox_data
            
            if not data_alvo_str: 
                incluir = False
            else:
                data_alvo = datetime.strptime(data_alvo_str, "%Y-%m-%d").date()
                
                if abrangencia == "Dia Específico":
                    incluir = (data_alvo == data_escolhida)
                elif abrangencia == "Mês Inteiro":
                    incluir = (data_alvo.month == data_escolhida.month and data_alvo.year == data_escolhida.year)
                elif abrangencia == "Ano Inteiro":
                    incluir = (data_alvo.year == data_escolhida.year)
                    
        # Se passou por todas as barreiras dos filtros, entra na tabela!
        if incluir:
            status = verificar_status(prox_data)
            
            linha = {
                "Matéria": item["materia"],
                "Cor": item.get("cor_materia", "transparent"), 
                "Tópico": item["topico"],
                "Data Teoria": item["data_teoria"],
                "Data Exame": item.get("data_exame", "Não definida"), 
                "Prev.": item["prevalencia"],
                "Diag. Questões": str(item["diag_questoes"]),
                "Diag. Acertos": str(item["diag_acertos"]),
                "Diag. Taxa": f"{item['diag_taxa']}%", 
            }
            
            for rev in item["revisoes"]:
                nome = rev["nome"]
                if rev["feita"]:
                    linha[f"Data {nome}"] = f"{rev['data']} ✅"
                    linha[f"Qts {nome}"] = str(rev["meta_questoes"])
                    linha[f"Acertos {nome}"] = str(rev["acertos"])
                    linha[f"Taxa {nome}"] = f"{rev['taxa']}%"
                else:
                    status_rev = verificar_status(rev["data"])
                    
                    if status_rev == "Atrasado":
                        linha[f"Data {nome}"] = f"{rev['data']} 🔴"
                    elif status_rev == "Hoje":
                        linha[f"Data {nome}"] = f"{rev['data']} 🎯"
                    else:
                        linha[f"Data {nome}"] = rev["data"]
                    
                    linha[f"Qts {nome}"] = str(rev["meta_questoes"]) if rev["meta_questoes"] > 0 else "-"
                    linha[f"Acertos {nome}"] = "-"
                    linha[f"Taxa {nome}"] = "-" 
                    
            linha["Próxima Revisão"] = f"{prox_data} ({prox_nome})" if prox_data else "Finalizado ✅"
            linha["Status"] = status
            
            linhas.append(linha)
            
    if not linhas:
        st.warning("Nenhum tópico encontrado para esses filtros. Tente mudá-los! 🕵️‍♂️")
        return

    df = pd.DataFrame(linhas)
    df = df.fillna("-")
    
    colunas = list(df.columns)
    if "Próxima Revisão" in colunas and "Status" in colunas:
        colunas.remove("Próxima Revisão")
        colunas.remove("Status")
        colunas_ordenadas = colunas + ["Próxima Revisão", "Status"]
        df = df[colunas_ordenadas] 

    # --- NOVO: EXPORTAÇÃO EXCEL (Acima da Tabela) ---
    buffer = io.BytesIO()
    # Removemos a coluna 'Cor' do arquivo Excel para ele ficar limpo
    df_para_excel = df.drop(columns=['Cor']) if 'Cor' in df.columns else df
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_para_excel.to_excel(writer, index=False, sheet_name='Meus Estudos')
    
    st.download_button(
        label="📊 Exportar Tabela para Excel",
        data=buffer.getvalue(),
        file_name=f"estudos_{datetime.now().strftime('%d-%m-%Y')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    # --- EXIBIÇÃO VISUAL (Igual ao seu original) ---
    def aplicar_estilos(row):
        estilos = []
        for col in row.index:
            bg_color = '#1e1e27' if row.name % 2 == 0 else '#2b2b36'
            if col == 'Matéria' and row['Cor'] != 'transparent':
                bg_color = row['Cor']
            estilos.append(f'background-color: {bg_color}')
        return estilos

    df_estilizado = df.style.apply(aplicar_estilos, axis=1)

    config_dinamica = {
        "Cor": None, 
        "Matéria": st.column_config.Column(pinned=True),
        "Tópico": st.column_config.Column(pinned=True)
    }
    
    for col in df.columns:
        if "Data" in col or "Revisão" in col:
            config_dinamica[col] = st.column_config.Column(width="medium")

    st.dataframe(
        df_estilizado, 
        use_container_width=False,
        column_config=config_dinamica
    )