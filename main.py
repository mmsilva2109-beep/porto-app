import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Porto Conectado", layout="wide")

# 2. Função de Leitura (Blindada contra erros de link)
def carregar_dados(url):
    try:
        id_planilha = url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv&gid=0"
        df = pd.read_csv(csv_url)
        # Padroniza os nomes das colunas: tudo minúsculo e sem espaços nas pontas
        df.columns = df.columns.str.strip().str.lower()
        return df
    except:
        return None

# 3. Interface
st.title("⚓ Sistema de Gestão Portuária")
st.markdown("---")

url_planilha = "https://docs.google.com/spreadsheets/d/15zVrF4-xy4sSb2WNG2asPEi2LKLuSCXxhqOBGSpEmAc/edit?usp=drivesdk"
df = carregar_dados(url_planilha)

busca = st.text_input("🔍 Consultar Booking (ex: BO-002):")

if busca and df is not None:
    # Busca o booking na coluna 'número de booking' (padronizada para minúsculo)
    col_booking = 'número de booking'
    
    if col_booking in df.columns:
        # Filtra ignorando maiúsculas/minúsculas
        resultado = df[df[col_booking].astype(str).str.strip().str.upper() == busca.strip().upper()]
        
        if not resultado.empty:
            d = resultado.iloc[0]
            st.success(f"✅ Booking {busca} localizado!")

            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🚚 Transporte")
                # O .get ajuda a não dar erro caso a coluna mude de nome
                st.info(f"**Motorista:** {d.get('nome do motorista', 'Não encontrado')}")
                st.write(f"**Cavalo:** {d.get('cavalo', '---')}")
                st.write(f"**Transportadora:** {d.get('transportadora', '---')}")
            
            with c2:
                st.subheader("📦 Carga")
                st.info(f"**Container:** {d.get('conteiner/refência', '---')}")
                st.write(f"**Navio:** {d.get('navio', '---')}")
                st.write(f"**Peso Bruto:** {d.get('peso bruto (kg)', '0')} KG")

            st.divider()
            if st.button("🚩 CONFIRMAR ENTRADA", use_container_width=True):
                st.balloons()
        else:
            st.error("❌ Booking não encontrado na planilha.")
    else:
        st.warning(f"⚠️ A coluna '{col_booking}' não foi achada. Verifique a linha 1 da planilha.")
elif busca and df is None:
    st.error("⚠️ Erro de conexão. Verifique se a planilha está como 'Qualquer pessoa com o link'.")




    

