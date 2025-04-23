import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Carregar dados
with open("dados.json", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df.columns = [col.strip() for col in df.columns]



# Limpar e converter valores monetários
def limpa_valor(valor):
    if isinstance(valor, str):
        return float(valor.replace("R$", "").replace(".", "").replace(",", ".").strip())
    return valor

colunas_monetarias = [
    "Aluguel", "Aluguel + Taxa", "Condominio com água", "Condominio",
    "ÁGUA", "IPTU", "TAXA BANC", "IPTU+ÁGUA", "condominio + Agua + IPTU", "Total BOLET"
]
for col in colunas_monetarias:
    df[col] = df[col].apply(limpa_valor)

# Verificação do vencimento
def verificar_vencimento(data_str):
    try:
        data_boleto = datetime.strptime(data_str, "%d/%m/%Y")
        hoje = datetime.now()
        return "✅ Em dia" if data_boleto >= hoje else "❌ Vencido"
    except:
        return "❓ Data inválida"

df["Status Vencimento"] = df["vencimento boleto"].apply(verificar_vencimento)

# Função para aplicar destaque em vermelho para boletos vencidos
def destaque_vencidos(row):
    if row["Status Vencimento"] == "❌ Vencido":
        return ["background-color: #ffcccc"] * len(row)
    else:
        return [""] * len(row)

# Exibir tabela com destaque
st.title("📊 Tabela de Boletos - Mês 04/2025")

formato_real = "R$ {:,.2f}".format
st.dataframe(
    df.style
    .format({col: formato_real for col in colunas_monetarias})
    .apply(destaque_vencidos, axis=1)
)

# Filtro por locatário
locatarios = df["Locatário"].unique()
loc_selecionado = st.selectbox("Filtrar por locatário", options=locatarios)
df_filtrado = df[df["Locatário"] == loc_selecionado]
st.dataframe(
    df_filtrado.style
    .format({col: formato_real for col in colunas_monetarias})
    .apply(destaque_vencidos, axis=1)
)


st.divider()
# Calcular total geral
total_geral = df["Total BOLET"].sum()

# Exibir um card com o total geral
st.markdown("### 💰 Total Geral dos Boletos")
st.metric(label="Valor total", value=f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
