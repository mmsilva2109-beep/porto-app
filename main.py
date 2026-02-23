import streamlit as st

# Configuração da página
st.set_page_config(page_title="Porto Conectado", layout="wide")

st.title("⚓ Sistema de Gestão Portuária")
st.markdown("---")

# Menu de Navegação
col1, col2, col3, col4 = st.columns(4)
with col1: btn_gate = st.button("🚛 GATE", use_container_width=True)
with col2: btn_patio = st.button("🏗️ PÁTIO", use_container_width=True)
with col3: btn_bordo = st.button("🚢 BORDO", use_container_width=True)
with col4: btn_chat = st.button("💬 CHAT", use_container_width=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "Início"

if btn_gate: st.session_state.pagina = "Gate"
if btn_patio: st.session_state.pagina = "Patio"
if btn_bordo: st.session_state.pagina = "Bordo"
if btn_chat: st.session_state.pagina = "Chat"

# Exibição das Telas
if st.session_state.pagina == "Gate":
    st.header("🚛 Registro de Gate")
    placa = st.text_input("Placa do Veículo")
    if st.button("Registrar Entrada"):
        st.success(f"Veículo {placa} registrado!")

elif st.session_state.pagina == "Patio":
    st.header("🏗️ Controle de Pátio")
    st.selectbox("Bloco de Destino", ["Zona A", "Zona B", "Zona C"])

elif st.session_state.pagina == "Bordo":
    st.header("🚢 Operação de Bordo")
    st.info("Navios atracados: MSC GIANNINA")

elif st.session_state.pagina == "Chat":
    st.header("💬 Comunicação Interna")
    st.text_area("Escreva um aviso para a equipe:")
    if st.button("Enviar"):
        st.toast("Mensagem enviada!")

