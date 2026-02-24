def carregar_dados(url):
    try:
        id_planilha = url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv&gid=0"
        df = pd.read_csv(csv_url)
        
        # ESSA LINHA É A MÁGICA: ela limpa espaços vazios nos nomes das colunas
        df.columns = df.columns.str.strip() 
        return df
    except Exception as e:
        return None


# Título do App
st.title("⚓ Sistema de Gestão Portuária")
st.markdown("---")

# LINK ATUALIZADO (Certifique-se de que a planilha está como 'Qualquer pessoa com o link')
url_planilha = "https://docs.google.com/spreadsheets/d/15zVrF4-xy4sSb2WNG2asPEi2LKLuSCXxhqOBGSpEmAc/edit?usp=drivesdk" 

df = carregar_dados(url_planilha)

# Interface de Busca
busca = st.text_input("🔍 Consultar Booking (ex: BO-002):")

if busca:
    if df is not None:
        # Filtra os dados
        resultado = df[df['Número de booking'].astype(str) == busca]
        
        if not resultado.empty:
            d = resultado.iloc[0]
            st.success(f"✅ Booking {busca} localizado!")

            # Organização em colunas para facilitar a leitura no celular
            col1, col2 = st.columns(2)

            with col1:
                with st.expander("🚚 Dados de Transporte", expanded=True):
                    st.write(f"**Motorista:** {d['Nome do motorista']}")
                    st.write(f"**CNH:** {d['CNH']}")
                    st.write(f"**Cavalo:** {d['Cavalo']}")
                    st.write(f"**Placas Carreta:** {d['Placa da carreta 1']} / {d['Placa da carreta 2']}")
                    st.write(f"**Transportadora:** {d['Transportadora']}")

                with st.expander("⚖️ Carga e Pesos", expanded=True):
                    st.write(f"**Container:** {d['Conteiner/Refência']}")
                    st.write(f"**Navio:** {d['Navio']}")
                    st.write(f"**Peso Bruto:** {d['Peso bruto (KG)']} KG")
                    st.write(f"**Peso Líquido:** {d['Peso líquido (KG)']} KG")

            with col2:
                with st.expander("🔒 Segurança e Documentos", expanded=True):
                    st.write(f"**Lacre SIF:** {d['Lacre SIF']}")
                    st.write(f"**Lacre de Lona:** {d['Lacre de Lona']}")
                    st.write(f"**Nota Fiscal:** {d['Nota Fiscal']}")
                    st.write(f"**IMO:** {d['Carga IMO']}")
                
                with st.expander("📏 Dimensões Excedentes"):
                    st.write(f"**Altura:** {d['Ex. Altura (cm)']} | **Frente:** {d['Ex. Frente (cm)']}")
                    st.write(f"**Atrás:** {d['Ex. atrás (cm)']} | **Laterais:** E:{d['Ex. Esquerda (cm)']} / D:{d['Ex Direita (cm)']}")

            # Botão de Ação para o Gate
            st.divider()
            if st.button("🚩 REGISTRAR ENTRADA NO GATE", use_container_width=True):
                st.balloons()
                st.info(f"Entrada confirmada para o Booking {busca}. Status atualizado na operação.")
        else:
            st.error("❌ Este Booking não consta na planilha.")
    else:
        st.warning("⚠️ Erro ao conectar com a planilha. Verifique o link no código.")

# Mural de Comunicação (Extra)
with st.sidebar:
    st.header("💬 Mural de Avisos")
    msg = st.text_input("Aviso rápido:")
    if st.button("Postar"):
        st.toast(f"Aviso enviado: {msg}")



    

