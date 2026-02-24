import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Porto Conectado", layout="wide")

# 2. Função de Leitura Ultra-Resistente
def carregar_dados(url):
    try:
        # Extrai o ID da planilha de qualquer link (celular ou PC)
        if "/d/" in url:
            id_planilha = url.split("/d/")[1].split("/")[0]
        else:
            return None
            
        # Força o link de exportação CSV da primeira aba (gid=0)
        csv_url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv&gid=0"
        
        # Lê os dados
        df = pd.read_csv(csv_url)
        
        # Limpa os nomes das colunas (tira espaços e deixa minúsculo)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        st.error(f"Erro na leitura: {e}")
        return None

# 3. Título
st.title("⚓ Sistema de Gestão Portuária")
st.markdown("---")

# Link da sua planilha
url_planilha = "https://docs.google.com/spreadsheets/d/15zVrF4-xy4sSb2WNG2asPEi2LKLuSCXxhqOBGSpEmAc/edit?usp=sharing"

df = carregar_dados(url_planilha)

busca = st.text_input("🔍 Consultar Booking (ex: BO-002):")

if busca:
    if df is not None:
        # Procuramos na coluna padronizada (minúscula)
        col_booking = 'número de booking'
        
        if col_booking in df.columns:
            # Busca ignorando espaços e letras grandes/pequenas
            filtro = df[col_booking].astype(str).str.strip().str.upper() == busca.strip().upper()
            resultado = df[filtro]
            
            if not resultado.empty:
                d = resultado.iloc[0]
                st.success(f"✅ Booking {busca} localizado!")

                # Exibição dos Dados
                c1, c2 = st.columns(2)
                with c1:
                    st.info("🚚 **Transporte**")
                    st.write(f"**Motorista:** {d.get('nome do motorista', 'N/A')}")
                    st.write(f"**Cavalo:** {d.get('cavalo', 'N/A')}")
                with c2:
                    st.info("📦 **Carga**")
                    st.write(f"**Container:** {d.get('conteiner/refência', 'N/A')}")
                    st.write(f"**Peso Bruto:** {d.get('peso bruto (kg)', '0')} KG")

                st.divider()
                if st.button("🚩 CONFIRMAR ENTRADA", use_container_width=True):
                    st.balloons()
            else:
                st.error("❌ Booking não encontrado na planilha.")
        else:
            st.warning(f"⚠️ A coluna '{col_booking}' não foi encontrada. Verifique os títulos na Linha 1 da planilha.")
    else:
        st.error("⚠️ Não foi possível carregar os dados. Verifique a internet ou o link.")






    

