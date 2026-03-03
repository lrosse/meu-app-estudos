import streamlit as st
from views import tabela, materias, adicionar, revisoes, gerenciar
from auth import verificar_login, registrar_usuario

# Configuração global da página do Streamlit
st.set_page_config(page_title="Sistema de Estudos", layout="wide", page_icon="📖")

# --- 1. CONTROLE DE SESSÃO (A "PULSEIRA VIP") ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = ""

# --- 2. TELA DE LOGIN/REGISTRO ---
if not st.session_state.logado:
    st.title("🔐 Acesso ao Sistema de Estudos")
    
    aba_login, aba_registro = st.tabs(["Entrar", "Criar Conta"])
    
    with aba_login:
        with st.form("form_login"):
            st.subheader("Fazer Login")
            user_login = st.text_input("Usuário")
            pass_login = st.text_input("Senha", type="password")
            
            if st.form_submit_button("Entrar"):
                if verificar_login(user_login, pass_login):
                    st.session_state.logado = True
                    st.session_state.usuario_logado = user_login
                    st.rerun() 
                else:
                    st.error("Usuário ou senha incorretos! ❌")
                    
    with aba_registro:
        with st.form("form_registro"):
            st.subheader("Criar Nova Conta")
            novo_user = st.text_input("Escolha um Nome de Usuário")
            nova_senha = st.text_input("Crie uma Senha", type="password")
            
            if st.form_submit_button("Registrar"):
                if not novo_user or not nova_senha:
                    st.error("Preencha todos os campos!")
                elif registrar_usuario(novo_user, nova_senha):
                    st.success("Conta criada com sucesso! 🎉 Vá na aba 'Entrar' para fazer login.")
                else:
                    st.error("Esse nome de usuário já está em uso! Tente outro.")
                    
    st.stop()

# =========================================================================
# --- 3. APLICATIVO PRINCIPAL ---
# =========================================================================

# --- A MÁGICA VISUAL: Truque Ninja de CSS ---
st.markdown(
    f"""
    <style>
    .cracha-flutuante {{
        position: fixed;
        top: 15px;
        right: 140px; /* Distância segura para fugir do menu Deploy */
        background-color: #2b2b36;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        border: 1px solid #4b4b5c;
        z-index: 9999999;
        font-size: 14px;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        transition: opacity 0.3s ease-in-out; /* Efeito suave ao aparecer/sumir */
    }}

    /* O SEGREDO: Se a página detectar que a barra lateral está expandida, ele oculta o crachá! */
    html:has([data-testid="stSidebar"][aria-expanded="true"]) .cracha-flutuante {{
        opacity: 0;
        pointer-events: none;
    }}
    </style>
    <div class="cracha-flutuante">👨‍🎓 {st.session_state.usuario_logado}</div>
    """,
    unsafe_allow_html=True
)

# --- AJUSTE DA BARRA LATERAL ---
# Saudação menor na barra lateral
st.sidebar.markdown(f"### 👨‍🎓 Olá, {st.session_state.usuario_logado}!")

# Damos um "pulo de linha" invisível para desgrudar do botão <<
st.sidebar.markdown("<br>", unsafe_allow_html=True) 

# Deixamos o botão de logout mais bonito, ocupando 100% da largura
if st.sidebar.button("🚪 Sair (Logout)", use_container_width=True):
    st.session_state.logado = False
    st.session_state.usuario_logado = ""
    st.rerun()

st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação", 
    [
        "Revisões de Hoje", 
        "Tabela Completa", 
        "Por Matéria", 
        "Adicionar Tópico", 
        "Gerenciar Tópicos"
    ]
)

if pagina == "Revisões de Hoje":
    revisoes.renderizar()
elif pagina == "Tabela Completa":
    tabela.renderizar()
elif pagina == "Por Matéria":
    materias.renderizar()
elif pagina == "Adicionar Tópico":
    adicionar.renderizar()
elif pagina == "Gerenciar Tópicos":
    gerenciar.renderizar()
