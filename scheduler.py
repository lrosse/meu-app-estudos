from datetime import datetime, timedelta

def calcular_taxa(acertos, questoes):
    if questoes == 0: return 0.0
    return round((acertos / questoes) * 100, 2)

def calcular_meta_questoes(prevalencia, taxa_anterior):
    meta = 10
    if prevalencia == "Alta": meta = 20 if taxa_anterior < 70 else 10
    elif prevalencia == "Média": meta = 15 if taxa_anterior < 70 else 8
    elif prevalencia == "Baixa": meta = 10 if taxa_anterior < 70 else 5
    return meta

def calcular_intervalo_dinamico(taxa, prevalencia, dias_pro_exame, num_revisao):
    """Calcula quantos dias até a próxima revisão baseado em TODOS os fatores."""
    # 1. Base (R1 = 3 dias, R2 = 7, R3 = 15, R4+ = 30)
    bases = {1: 3, 2: 7, 3: 15}
    dias_base = bases.get(num_revisao, 30)

    # 2. Fator Taxa (Acertou muito = adia; Errou muito = puxa pra perto)
    mult_taxa = 1.0
    if taxa < 50: mult_taxa = 0.5
    elif taxa < 75: mult_taxa = 0.8
    elif taxa >= 85: mult_taxa = 1.5

    # 3. Fator Prevalência (Alta = revisa com mais frequência)
    mult_prev = 1.0
    if prevalencia == "Alta": mult_prev = 0.7
    elif prevalencia == "Baixa": mult_prev = 1.3

    intervalo = max(1, round(dias_base * mult_taxa * mult_prev))

    # 4. Fator Desespero Pré-Prova! (Se falta menos de 30 dias, acelera!)
    if 0 < dias_pro_exame <= 30:
        intervalo = max(1, intervalo // 2)

    return intervalo

def recalcular_cronograma(revisoes, taxa_atual, prevalencia, data_exame_str, data_teoria_str):
    """Projeta ou atualiza todas as datas futuras do cronograma como um GPS."""
    data_exame = datetime.strptime(data_exame_str, "%Y-%m-%d").date()
    hoje = datetime.now().date()
    
    # A base de tempo começa na Teoria. Se houver revisão feita, a base avança.
    ultima_data_base = datetime.strptime(data_teoria_str, "%Y-%m-%d").date()

    for i, rev in enumerate(revisoes):
        if rev["feita"]:
            ultima_data_base = datetime.strptime(rev["data"], "%Y-%m-%d").date()
            continue

        num_revisao = i + 1
        dias_pro_exame = (data_exame - ultima_data_base).days
        
        intervalo = calcular_intervalo_dinamico(taxa_atual, prevalencia, dias_pro_exame, num_revisao)
        nova_data = ultima_data_base + timedelta(days=intervalo)

        # Se o algoritmo projetar a revisão para DEPOIS da prova, nós forçamos ela para ANTES da prova
        if nova_data >= data_exame:
            # Coloca a revisão pra metade do tempo que falta pra prova
            nova_data = data_exame - timedelta(days=max(1, dias_pro_exame // 2))

        # Se, por causa do recálculo, a data cair no passado, jogamos para amanhã
        if nova_data <= hoje and num_revisao > 1:
            nova_data = hoje + timedelta(days=1)

        rev["data"] = nova_data.strftime("%Y-%m-%d")
        if rev["meta_questoes"] == 0:
            rev["meta_questoes"] = calcular_meta_questoes(prevalencia, taxa_atual)
            
        ultima_data_base = nova_data # A próxima revisão usará essa data como base

def gerar_revisoes(data_teoria_str, data_exame_str, taxa_diag, prevalencia):
    """Cria a 'casca' das revisões iniciais e pede pro GPS calcular as rotas."""
    revisoes = [
        {"nome": "R1", "data": "", "feita": False, "meta_questoes": 0, "acertos": 0, "taxa": 0.0},
        {"nome": "R2", "data": "", "feita": False, "meta_questoes": 0, "acertos": 0, "taxa": 0.0},
        {"nome": "R3", "data": "", "feita": False, "meta_questoes": 0, "acertos": 0, "taxa": 0.0},
        {"nome": "R4", "data": "", "feita": False, "meta_questoes": 0, "acertos": 0, "taxa": 0.0}
    ]
    recalcular_cronograma(revisoes, taxa_diag, prevalencia, data_exame_str, data_teoria_str)
    return revisoes

def calcular_proxima_revisao(revisoes):
    for rev in revisoes:
        if not rev["feita"]: return rev["data"], rev["nome"]
    return None, "Finalizado"

def verificar_status(data_revisao_str):
    if not data_revisao_str: return "Concluído"
    hoje = datetime.now().date()
    data_rev = datetime.strptime(data_revisao_str, "%Y-%m-%d").date()
    if data_rev < hoje: return "Atrasado"
    elif data_rev == hoje: return "Hoje"
    return "Futuro"