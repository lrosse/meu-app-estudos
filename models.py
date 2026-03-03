import uuid

# Adicionamos o campo data_exame
def criar_topico(materia, topico, data_teoria, data_exame, prevalencia, questoes_diag, acertos_diag, taxa_diag, revisoes, cor_materia="transparent"):
    return {
        "id": str(uuid.uuid4()),
        "materia": materia,
        "cor_materia": cor_materia,
        "topico": topico,
        "data_teoria": data_teoria,
        "data_exame": data_exame, # <- NOVO!
        "prevalencia": prevalencia,
        "diag_questoes": questoes_diag,
        "diag_acertos": acertos_diag,
        "diag_taxa": taxa_diag,
        "revisoes": revisoes  
    }