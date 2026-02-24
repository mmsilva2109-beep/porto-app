import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Porto Conectado", layout="wide")

# Função de Leitura Direta
def carregar_dados():
    try:
        # Link direto de exportação (ajustado para ser o mais simples possível)
        id_planilha = "15zVrF4-xy4sSb2WNG2asPEi2LKLuSCXxhqOBGSpEmAc"
        url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/gviz/tq?tqx=out:csv"
        
        df = pd.read_csv(url)
        # Limpa os nomes das colunas
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        st.error(f"Erro ao acessar dados: {e}")
        return None

st.title("⚓ Sistema de Gestão Portuária")
st.markdown("---")

df = carregar_dados()

busca = st.text_input("🔍 Digite o Booking (ex: BO-002):")

if busca:
    if df is not None:
        # Procura na coluna 'número de booking'
        col_booking = 'número de booking'
        
        # Filtra ignorando maiúsculas e espaços
        resultado = df[df[col_booking].astype(str).str.strip().str.upper() == busca.strip().upper()]
        
        if not resultado.empty:
            d = resultado.iloc[0]
            st.success(f"✅ Booking {busca} localizado!")

            c1, c2 = st.columns(2)
            with c1:
                st.info("🚚 **Transporte**")
                st.write(f"**Motorista:** {d.get('nome do motorista', 'N/A')}")
                st.write(f"**Cavalo:** {d.get('cavalo', 'N/A')}")
            with c2:
                st.info("📦 **Carga**")
                st.write(f"**Container:** {d.get('conteiner/refência', 'N/A')}")
                st.write(f"**Navio:** {d.get('navio', 'N/A')}")

            st.divider()
            if st.button("🚩 CONFIRMAR ENTRADA", use_container_width=True):
                st.balloons()
                st.success("Entrada Registrada com Sucesso!")
        else:
            st.error("❌ Booking não encontrado. Verifique se ele está na planilha.")
    else:
        st.error("⚠️ Não foi possível carregar a planilha.")



    

