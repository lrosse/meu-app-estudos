import streamlit as st
from storage import load_data, save_data
from scheduler import calcular_proxima_revisao, verificar_status, calcular_taxa, recalcular_cronograma
from datetime import datetime

def renderizar():
    st.header("⏰ Revisões Pendentes")
    dados = load_data()
    if not dados: return st.info("Não há dados cadastrados.")
        
    pendentes = [(i, item, *calcular_proxima_revisao(item["revisoes"])) for i, item in enumerate(dados)]
    pendentes = [(i, it, d, n, verificar_status(d)) for i, it, d, n in pendentes if verificar_status(d) in ["Hoje", "Atrasado"]]
            
    if not pendentes:
        return st.success("Tudo em dia! Nenhuma revisão pendente para hoje. 🎉")
        
    for idx, item, data_rev, nome_rev, status in pendentes:
        rev_atual = next(r for r in item["revisoes"] if r["nome"] == nome_rev)
        
        with st.expander(f"[{status.upper()}] {item['materia']} - {item['topico']} ({nome_rev})", expanded=True):
            data_exame_str = item.get('data_exame', 'Não definida')
            st.write(f"**Data da Prova:** {data_exame_str} 🎯")
            
            # Se a taxa anterior foi ruim, damos um aviso!
            if rev_atual['meta_questoes'] >= 15:
                st.warning("⚠️ O GPS detectou que você precisa de foco neste assunto. Carga de exercícios aumentada!")

            st.write(f"**Meta sugerida:** {rev_atual['meta_questoes']} questões.")
            
            with st.form(f"form_rev_{item['id']}"):
                col1, col2 = st.columns(2)
                qts = col1.number_input("Questões feitas", min_value=1, value=rev_atual['meta_questoes'], step=1)
                acts = col2.number_input("Acertos", min_value=0, max_value=int(qts), step=1)
                
                if st.form_submit_button("Concluir Revisão"):
                    # 1. Salva os resultados
                    rev_atual["feita"] = True
                    rev_atual["meta_questoes"] = qts
                    rev_atual["acertos"] = acts
                    rev_atual["taxa"] = calcular_taxa(acts, qts)
                    
                    # 2. VERIFICAÇÃO INTELIGENTE (Sem freio de mão exagerado)
                    todas_feitas = all(r["feita"] for r in item["revisoes"])
                    
                    if data_exame_str != "Não definida":
                        dias_pra_prova = (datetime.strptime(data_exame_str, "%Y-%m-%d").date() - datetime.now().date()).days
                    else:
                        dias_pra_prova = 999
                    
                    # CORREÇÃO AQUI: Gera nova revisão se faltar pelo menos 2 dias para a prova
                    if todas_feitas and dias_pra_prova >= 2:
                        num_nova_rev = len(item["revisoes"]) + 1
                        item["revisoes"].append({
                            "nome": f"R{num_nova_rev}", "data": "", "feita": False, 
                            "meta_questoes": 0, "acertos": 0, "taxa": 0.0
                        })
                    
                    # 3. RECALCULA O CRONOGRAMA
                    recalcular_cronograma(item["revisoes"], rev_atual["taxa"], item["prevalencia"], data_exame_str, item["data_teoria"])
                            
                    save_data(dados)
                    st.success("Revisão registrada! O GPS recalculou suas rotas. 🚗")
                    st.rerun()