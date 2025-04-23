import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Boletos Condominiais", layout="wide")
st.title("Planilha Condominial 📊")

# Ler os dados do arquivo JSON
try:
    with open("dados.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        df = pd.DataFrame(data)
except FileNotFoundError:
    st.error("O arquivo 'dados.json' não foi encontrado.")
    st.stop()

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



with st.container():
    st.subheader("📄 Tabela Completa")
    st.dataframe(
        df.style
        .format({col: formato_real for col in colunas_monetarias if col in df.columns})
        .apply(destaque_vencidos, axis=1),
        use_container_width=True
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
            .apply(destaque_vencidos, axis=1),
            use_container_width=True
        )




with st.container():
    st.subheader("🏢 Total de Boletos por Locatário")

    # Agrupamento por locatário
    total_por_locatario = (
        df.groupby("Locatário")["Total BOLET"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    ).rename(columns={"Total BOLET": "Total (R$)"})

    # Formatar os valores monetários
    total_por_locatario["Total (R$)"] = total_por_locatario["Total (R$)"].apply(formato_real)

    # Adicionar uma linha com o total geral
    total_geral = df["Total BOLET"].sum()
    total_por_locatario = pd.concat([
        total_por_locatario,
        pd.DataFrame([{"Locatário": "Total Geral", "Total (R$)": formato_real(total_geral)}])
    ], ignore_index=True)

    # Exibir a tabela
    st.dataframe(total_por_locatario, use_container_width=True)

 # Layout com containers
    with st.container():
        if "Total BOLET" in df.columns:
            total_geral = df["Total BOLET"].sum()
            st.metric("💰 Total Geral dos Boletos", value=f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
