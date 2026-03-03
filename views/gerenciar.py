import streamlit as st
from storage import load_data, save_data

def hex_to_rgba(hex_color, opacity=0.25):
    """Converte HEX do painel para RGBA transparente."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {opacity})'

def rgba_to_hex(rgba_str):
    """Converte o RGBA salvo de volta para HEX para o painel de cores ler."""
    if rgba_str == "transparent" or not rgba_str.startswith("rgba"):
        return "#3b82f6" # Azul padrão se não tiver cor
    try:
        parts = rgba_str.replace("rgba(", "").replace(")", "").split(",")
        r, g, b = int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip())
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return "#3b82f6"

def renderizar():
    st.header("⚙️ Gerenciar Tópicos")
    
    dados = load_data()
    if not dados:
        st.info("Nenhum tópico cadastrado para gerenciar.")
        return
        
    # Cria uma lista formatada para facilitar a busca no selectbox
    opcoes = [f"{i} - {item['materia']} ({item['topico']})" for i, item in enumerate(dados)]
    
    st.subheader("Selecione um tópico para Editar ou Excluir:")
    escolha = st.selectbox("Buscar Tópico cadastrado", opcoes)
    
    # Extrai o índice (ID) numérico do tópico que o usuário escolheu
    idx = int(escolha.split(" - ")[0])
    item_atual = dados[idx]
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # --- COLUNA 1: EDIÇÃO ---
    with col1:
        st.subheader("✏️ Editar Informações")
        with st.form(f"form_editar"):
            # Os campos já vêm preenchidos com os dados atuais!
            nova_materia = st.text_input("Matéria", value=item_atual["materia"])
            novo_topico = st.text_input("Tópico", value=item_atual["topico"])
            
            # Puxamos a cor atual convertendo para HEX
            cor_atual_hex = rgba_to_hex(item_atual.get("cor_materia", "transparent"))
            nova_cor_hex = st.color_picker("Cor da Matéria", cor_atual_hex)
            
            btn_salvar = st.form_submit_button("Salvar Alterações")
            
            if btn_salvar:
                if not nova_materia or not novo_topico:
                    st.error("Matéria e Tópico não podem ficar em branco!")
                else:
                    dados[idx]["materia"] = nova_materia
                    dados[idx]["topico"] = novo_topico
                    dados[idx]["cor_materia"] = hex_to_rgba(nova_cor_hex)
                    
                    save_data(dados)
                    st.success("Tópico atualizado com sucesso!")
                    st.rerun() # Atualiza a página instantaneamente
                    
    # --- COLUNA 2: EXCLUSÃO ---
    with col2:
        st.subheader("🗑️ Excluir Tópico")
        st.warning("⚠️ Atenção: Excluir um tópico apagará todo o histórico de revisões dele. Esta ação não pode ser desfeita.")
        
        # O type="primary" deixa o botão vermelho no tema escuro do Streamlit
        if st.button("Excluir Tópico Definitivamente", type="primary"):
            dados.pop(idx) # Remove o item da lista
            save_data(dados)
            st.success("Tópico excluído com sucesso!")
            st.rerun()