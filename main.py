import streamlit as st
import pandas as pd

st.set_page_config(page_title="Porto Conectado", layout="wide")

# Função para ler a planilha (Substitua pelo seu link)
def carregar_dados(url):
    try:
        csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
        return pd.read_csv(csv_url)
    except:
        return None

st.title("⚓ Sistema de Consulta e Gate")

# --- COLE O SEU LINK DA PLANILHA AQUI ---
url_planilha = "URL_DA_SUA_PLANILHA"

df = carregar_dados(url_planilha)

if df is not None:
    busca_booking = st.text_input("🔍 Digite o Número do Booking (Ex: BO-002):")

    if busca_booking:
        # Filtra na coluna exata que você passou
        resultado = df[df['Número de booking'] == busca_booking]

        if not resultado.empty:
            st.success("✅ Booking Localizado!")
            d = resultado.iloc[0]

            # --- ORGANIZAÇÃO DAS INFORMAÇÕES CONFORME SUA PLANILHA ---
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("🚛 Transporte")
                st.write(f"**Motorista:** {d['Nome do motorista']}")
                st.write(f"**Cavalo:** {d['Cavalo']}")
                st.write(f"**Transportadora:** {d['Transportadora']}")
                st.write(f"**Placas Carreta:** {d['Placa da carreta 1']} / {d['Placa da carreta 2']}")

            with col2:
                st.subheader("📦 Carga e Pesos")
                st.write(f"**Container:** {d['Conteiner/Refência']}")
                st.write(f"**Navio:** {d['Navio']}")
                st.write(f"**Peso Bruto:** {d['Peso bruto (KG)']} KG")
                st.write(f"**Peso Líquido:** {d['Peso líquido (KG)']} KG")

            with col3:
                st.subheader("🔒 Segurança e Medidas")
                st.write(f"**Lacre SIF:** {d['Lacre SIF']}")
                st.write(f"**Lacre Lona:** {d['Lacre de Lona']}")
                st.write(f"**NF:** {d['Nota Fiscal']}")
                st.write(f"**Carga IMO:** {d['Carga IMO']}")

            st.divider()
            
            # --- ÁREA DO GATE (SUGESTÃO DE REGISTRO) ---
            st.subheader("📝 Registro de Entrada (Gate)")
            c_gate1, c_gate2 = st.columns(2)
            lacre_conf = c_gate1.text_input("Confirme o Lacre Físico na entrada")
            avaria = c_gate2.selectbox("Avarias?", ["Não", "Sim - Amassado", "Sim - Rasgado/Furado"])
            
            if st.button("CONFIRMAR ENTRADA NO PORTO"):
                st.balloons()
                st.success(f"Entrada do Booking {busca_booking} registrada às {st.session_state.get('hora_atual', 'agora')}!")
        else:
            st.error("❌ Booking não encontrado. Verifique se digitou corretamente (ex: BO-001).")
else:
    st.info("💡 Por favor, conecte o link da sua planilha no código para visualizar os dados.")

    

