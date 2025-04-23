import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Boletos Condominiais", layout="wide")
st.title("Planilha Condominial 📊")

# Upload do arquivo
uploaded_file = st.file_uploader("Selecione um arquivo JSON, CSV ou Excel", type=["json", "csv", "xlsx"])

if uploaded_file is not None:
    # Detectar o tipo e ler
    if uploaded_file.name.endswith(".json"):
        data = json.load(uploaded_file)
        df = pd.DataFrame(data)
    elif uploaded_file.name.endswith(".csv"):
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    df.columns = [col.strip() for col in df.columns]

    # Limpeza de valores monetários
    def limpa_valor(valor):
        if isinstance(valor, str):
            return float(valor.replace("R$", "").replace(".", "").replace(",", ".").strip())
        return valor

    colunas_monetarias = [
        "Aluguel", "Aluguel + Taxa", "Condominio com água", "Condominio",
        "ÁGUA", "IPTU", "TAXA BANC", "IPTU+ÁGUA", "condominio + Agua + IPTU", "Total BOLET"
    ]
    for col in colunas_monetarias:
        if col in df.columns:
            df[col] = df[col].apply(limpa_valor)

    # Verificação de vencimento
    def verificar_vencimento(data_str):
        try:
            data_boleto = datetime.strptime(data_str, "%d/%m/%Y")
            return "✅ Em dia" if data_boleto >= datetime.now() else "❌ Vencido"
        except:
            return "❓ Data inválida"

    if "vencimento boleto" in df.columns:
        df["Status Vencimento"] = df["vencimento boleto"].apply(verificar_vencimento)

    # Estilo para vencidos
    def destaque_vencidos(row):
        return ["background-color: #ffcccc"] * len(row) if row.get("Status Vencimento") == "❌ Vencido" else [""] * len(row)

    formato_real = "R$ {:,.2f}".format

    # Layout com containers
    with st.container():
        if "Total BOLET" in df.columns:
            total_geral = df["Total BOLET"].sum()
            st.metric("💰 Total Geral dos Boletos", value=f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    with st.container():
        st.subheader("📄 Tabela Completa")
        st.dataframe(
            df.style
            .format({col: formato_real for col in colunas_monetarias if col in df.columns})
            .apply(destaque_vencidos, axis=1)
        )

    with st.container():
        if "Locatário" in df.columns:
            st.subheader("🔍 Filtro por Locatário")
            locatarios = df["Locatário"].unique()
            loc_selecionado = st.selectbox("Selecione um locatário", options=locatarios)
            df_filtrado = df[df["Locatário"] == loc_selecionado]
            st.dataframe(
                df_filtrado.style
                .format({col: formato_real for col in colunas_monetarias if col in df.columns})
                .apply(destaque_vencidos, axis=1)
            )



else:
    st.info("⬆️ Envie um arquivo JSON, CSV ou Excel para visualizar os dados.")


with st.container():
    st.subheader("🏢 Total de Boletos por Locatário")

    # Agrupamento
    total_por_locatario = (
        df.groupby("Locatário")["Total BOLET"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    ).rename(columns={"Total BOLET": "Total"})

    # Seletor de quantidade
    quantidade = st.slider(
        "Quantos locatários deseja exibir?",
        min_value=5,
        max_value=min(30, len(total_por_locatario)),
        value=10,
        step=1
    )

    dados_filtrados = total_por_locatario.head(quantidade)

    # Gráfico com Altair
    import altair as alt
    chart = alt.Chart(dados_filtrados).mark_bar().encode(
        x=alt.X("Total:Q", title="Total (R$)"),
        y=alt.Y("Locatário:N", sort="-x"),
        tooltip=["Locatário", "Total"]
    ).properties(width=700, height=400)

    st.altair_chart(chart, use_container_width=True)

