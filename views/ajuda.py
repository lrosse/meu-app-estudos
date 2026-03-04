import streamlit as st

def renderizar():
    st.header("❓ Ajuda — Como usar o Sistema de Estudos")

    st.markdown("""
    > 👋 **Bem-vindo ao seu assistente de estudos inteligente!**  
    > Este sistema foi criado para te ajudar a estudar de forma mais eficiente,  
    > lembrando **quando revisar** cada assunto para que você não esqueça o que aprendeu.
    """)

    st.markdown("---")

    # -----------------------------------------------------------------------
    # 1. O QUE É ESSE SISTEMA?
    # -----------------------------------------------------------------------
    with st.expander("📖 O que é esse sistema e para que serve?", expanded=True):
        st.markdown("""
        Quando estudamos algo novo, nosso cérebro tende a esquecer com o tempo — isso é normal!  
        A ciência mostra que **revisar o conteúdo nos momentos certos** faz com que ele fique gravado  
        na memória de longo prazo. Esse fenômeno se chama **Repetição Espaçada**.

        Este sistema aplica exatamente isso: ele **calcula automaticamente as melhores datas**  
        para você revisar cada tópico, levando em conta:

        - 📅 Quando você estudou o assunto pela primeira vez  
        - 🎯 Qual é a data da sua prova  
        - 📊 Seu desempenho nas questões (quanto mais acertou, mais tempo até a próxima revisão)  
        - ⚠️ A importância do assunto para a prova (Alta, Média ou Baixa prevalência)

        **O resultado?** Você estuda menos horas, mas retém muito mais!
        """)

    # -----------------------------------------------------------------------
    # 2. PRIMEIRO ACESSO
    # -----------------------------------------------------------------------
    with st.expander("🔐 Criando sua conta e fazendo login"):
        st.markdown("""
        Na tela inicial você verá duas abas: **Entrar** e **Criar Conta**.

        **Para criar sua conta:**
        1. Clique na aba **"Criar Conta"**
        2. Escolha um nome de usuário (sem espaços, ex: `joao123`)
        3. Crie uma senha
        4. Clique em **"Registrar"**
        5. Pronto! Agora vá para a aba **"Entrar"** e faça login

        > 🔒 Seus dados ficam salvos separadamente dos outros usuários.  
        > Ninguém vê o que você cadastrou — é tudo seu!
        """)

    # -----------------------------------------------------------------------
    # 3. ADICIONANDO UM TÓPICO
    # -----------------------------------------------------------------------
    with st.expander("➕ Como adicionar um tópico de estudo"):
        st.markdown("""
        Após o login, vá no menu lateral esquerdo e clique em **"Adicionar Tópico"**.

        Preencha os campos:

        | Campo | O que colocar |
        |---|---|
        | **Matéria** | Ex: Cardiologia, Direito Civil, Matemática |
        | **Tópico** | Ex: Insuficiência Cardíaca, Contratos, Equações |
        | **Data da Teoria** | O dia em que você estudou/vai estudar esse assunto |
        | **Data da Prova/Exame** | A data da sua prova — o sistema usa isso para calcular as revisões |
        | **Prevalência** | Quão importante é esse assunto para a prova (Alta, Média ou Baixa) |
        | **Questões diagnóstico** | Quantas questões você fez sobre esse assunto |
        | **Acertos diagnóstico** | Quantas você acertou |
        | **Cor da matéria** | Uma cor para identificar visualmente a matéria na tabela |

        Depois clique em **"Salvar Tópico"** — o sistema já vai gerar o cronograma de revisões automaticamente! 🎉

        > 💡 **Dica:** Se você ainda não fez questões diagnóstico, coloque **0** nos dois campos.  
        > O sistema irá sugerir uma quantidade adequada na primeira revisão.
        """)

    # -----------------------------------------------------------------------
    # 4. REVISÕES DE HOJE
    # -----------------------------------------------------------------------
    with st.expander("⏰ Revisões de Hoje — sua tela principal do dia a dia"):
        st.markdown("""
        Esta é a tela que você deve abrir **todo dia** antes de estudar.

        Ela mostra apenas os tópicos que precisam ser revisados **hoje ou que estão atrasados**.

        **Como funciona:**
        1. Abra o sistema e vá em **"Revisões de Hoje"**
        2. Veja quais tópicos aparecem (se não aparecer nenhum — parabéns, você está em dia! ✅)
        3. Para cada tópico listado, faça as questões sugeridas
        4. Volte ao sistema, preencha **quantas questões fez** e **quantas acertou**
        5. Clique em **"Concluir Revisão"**

        O sistema vai recalcular automaticamente quando será a próxima revisão desse tópico,  
        baseado no seu desempenho. **Se foi bem → próxima revisão mais longe. Se foi mal → mais perto.**

        > 🚗 Pense no sistema como um GPS de estudos: se você "errou o caminho" (foi mal nas questões),  
        > ele recalcula a rota para te colocar de volta nos trilhos!
        """)

    # -----------------------------------------------------------------------
    # 5. TABELA COMPLETA
    # -----------------------------------------------------------------------
    with st.expander("📋 Tabela Completa — visão geral de tudo"):
        st.markdown("""
        Em **"Tabela Completa"** você vê todos os seus tópicos cadastrados em uma tabela detalhada,  
        com datas de revisão, taxas de acerto e status.

        **Filtros disponíveis:**
        - Filtrar por **matéria específica**
        - Filtrar por **data da teoria** ou **próxima revisão**
        - Ver tópicos de um **dia**, **mês** ou **ano** específico

        Você também pode **exportar tudo para Excel** clicando no botão  
        📊 *"Exportar Tabela para Excel"* — útil para guardar seu histórico ou compartilhar.

        **Ícones de status na tabela:**
        - 🔴 Atrasado — revisão passou da data e ainda não foi feita
        - 🎯 Hoje — revisão está marcada para hoje
        - ✅ Feita — revisão já foi concluída
        """)

    # -----------------------------------------------------------------------
    # 6. POR MATÉRIA
    # -----------------------------------------------------------------------
    with st.expander("📚 Por Matéria — acompanhe seu progresso"):
        st.markdown("""
        Em **"Por Matéria"** você escolhe uma matéria e vê todos os tópicos dela,  
        com uma **barra de progresso** mostrando sua taxa geral de acertos.

        É uma boa forma de identificar quais matérias precisam de mais atenção.

        > 🟢 Barras mais verdes = você está indo bem  
        > ⬜ Barras curtas = precisa revisar mais
        """)

    # -----------------------------------------------------------------------
    # 7. GERENCIAR TÓPICOS
    # -----------------------------------------------------------------------
    with st.expander("⚙️ Gerenciar Tópicos — editar ou excluir"):
        st.markdown("""
        Em **"Gerenciar Tópicos"** você pode:

        - ✏️ **Editar** o nome da matéria, do tópico ou a cor
        - 🗑️ **Excluir** um tópico que não é mais necessário

        > ⚠️ **Atenção:** Excluir um tópico apaga todo o histórico de revisões dele.  
        > Essa ação **não pode ser desfeita**, então tenha certeza antes de confirmar!
        """)

    # -----------------------------------------------------------------------
    # 8. DICAS GERAIS
    # -----------------------------------------------------------------------
    with st.expander("💡 Dicas para aproveitar ao máximo"):
        st.markdown("""
        **✅ Boas práticas:**
        - Abra o sistema **todos os dias** e verifique "Revisões de Hoje"
        - Cadastre os tópicos **logo após estudá-los**, enquanto ainda está fresco
        - Seja honesto nos acertos — o sistema só funciona bem com dados reais
        - Coloque a **data correta da prova** para o cronograma ser calculado certo

        **🚫 Evite:**
        - Deixar revisões acumularem — quanto mais atrasado, menos eficiente fica
        - Colocar datas de prova erradas (o sistema adapta tudo em cima delas)
        - Cadastrar o mesmo tópico duas vezes

        **📱 Pode usar no celular?**  
        Sim! O sistema funciona em qualquer navegador, incluindo pelo celular.  
        Basta acessar o mesmo link que você usa no computador.
        """)

    # -----------------------------------------------------------------------
    # RODAPÉ
    # -----------------------------------------------------------------------
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 13px;'>
        📖 Sistema de Estudos com Repetição Espaçada<br>
        Dúvidas ou sugestões? Fale com o desenvolvedor do sistema.
    </div>
    """, unsafe_allow_html=True)