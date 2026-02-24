import streamlit as st
import pandas as pd

# 1. Configuração Inicial
st.set_page_config(page_title="Porto Conectado", layout="wide")

def carregar_dados(url):
    try:
        id_planilha = url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv&gid=0"
        df = pd.read_csv(csv_url)
        # Limpa nomes das colunas (tira espaços e deixa tudo minúsculo)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        return None

# 2. Interface Principal
st.title("⚓ Sistema de Gestão Portuária")
st.markdown("---")

# link da sua planilha
url_planilha = "https://docs.google.com/spreadsheets/d/15zVrF4-xy4sSb2WNG2asPEi2LKLuSCXxhqOBGSpEmAc/edit?usp=sharing" 

df = carregar_dados(url_planilha)

busca = st.text_input("🔍 Consultar Booking (ex: BO-002):")

if busca:
    if df is not None:
        # Busca o booking ignorando maiúsculas/minúsculas
        coluna_booking = 'número de booking' # nome da coluna na planilha em minúsculo
        
        if coluna_booking in df.columns:
            resultado = df[df[coluna_booking].astype(str).str.upper() == busca.upper()]
            
            if not resultado.empty:
                d = resultado.iloc[0]
                st.success(f"✅ Booking {busca} localizado!")

                col1, col2 = st.columns(2)
                with col1:
                    with st.expander("🚚 Dados de Transporte", expanded=True):
                        # Usamos .get() para não dar erro se a coluna não existir
                        st.write(f"**Motorista:** {d.get('nome do motorista', 'Não informado')}")
                        st.write(f"**Cavalo:** {d.get('cavalo', 'Não informado')}")
                        st.write(f"**Transportadora:** {d.get('transportadora', 'Não informado')}")

                with col2:
                    with st.expander("⚖️ Carga e Pesos", expanded=True):
                        st.write(f"**Container:** {d.get('conteiner/refência', 'Não informado')}")
                        st.write(f"**Navio:** {d.get('navio', 'Não informado')}")
                        st.metric("Peso Bruto (KG)", d.get('peso bruto (kg)', '0'))

                st.divider()
                if st.button("🚩 REGISTRAR ENTRADA NO GATE", use_container_width=True):
                    st.balloons()
                    st.info("Entrada registrada com sucesso!")
            else:
                st.error("❌ Booking não encontrado na planilha.")
        else:
            st.warning(f"⚠️ A coluna '{coluna_booking}' não foi encontrada na planilha. Verifique os títulos da primeira linha.")
    else:
        st.error("⚠️ Erro de conexão com a planilha.")



    

