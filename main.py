import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Porto Conectado", layout="wide")

# 2. Função de Leitura Robusta
def carregar_dados(url):
    try:
        # Extrai apenas o ID da planilha para evitar erros de link do celular
        id_planilha = url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv&gid=0"
        df = pd.read_csv(csv_url)
        # Padroniza títulos: tudo minúsculo e sem espaços extras
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        return None

# 3. Interface Principal
st.title("⚓ Sistema de Gestão Portuária")
st.markdown("---")

# Link da sua planilha (Já ajustado para o ID correto)
url_planilha = "https://docs.google.com/spreadsheets/d/15zVrF4-xy4sSb2WNG2asPEi2LKLuSCXxhqOBGSpEmAc/edit?usp=sharing"

df = carregar_dados(url_planilha)

busca = st.text_input("🔍 Consultar Booking (ex: BO-002):")

if busca:
    if df is not None:
        # Busca o booking ignorando espaços e letras grandes/pequenas
        col_booking = 'número de booking'
        
        if col_booking in df.columns:
            # Filtro inteligente
            resultado = df[df[col_booking].astype(str).str.strip().str.upper() == busca.strip().upper()]
            
            if not resultado.empty:
                d = resultado.iloc[0]
                st.success(f"✅ Booking {busca} localizado!")

                c1, c2 = st.columns(2)
                with c1:
                    with st.expander("🚚 Dados de Transporte", expanded=True):
                        st.info(f"**Motorista:** {d.get('nome do motorista', '---')}")
                        st.write(f"**Cavalo:** {d.get('cavalo', '---')}")
                        st.write(f"**Transportadora:** {d.get('transportadora', '---')}")
                
                with c2:
                    with st.expander("📦 Carga e Pesos", expanded=True):
                        st.info(f"**Container:** {d.get('conteiner/refência', '---')}")
                        st.write(f"**Navio:** {d.get('navio', '---')}")
                        st.write(f"**Peso Bruto:** {d.get('peso bruto (kg)', '0')} KG")

                st.divider()
                if st.button("🚩 CONFIRMAR ENTRADA NO GATE", use_container_width=True):
                    st.balloons()
                    st.success("Entrada Registrada!")
            else:
                st.error("❌ Booking não encontrado na planilha. Verifique se digitou corretamente.")
        else:
            st.error(f"⚠️ A coluna '{col_booking}' não foi encontrada na sua planilha. Verifique a primeira linha.")
    else:
        st.error("⚠️ Erro de conexão. Verifique se a planilha tem dados na primeira aba.")





    

