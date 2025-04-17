import streamlit as st
import dados
import pandas as pd
import numpy as np


# Configurações da página
st.set_page_config(page_title="Gestão de Apartamentos", layout="wide", initial_sidebar_state="expanded")

# Menu lateral
st.sidebar.title("Menu")
pagina = st.sidebar.radio("Navegação", ["Dados", "Planilha Geral de Condominio"])

# Página: Cadastro
if pagina == "Planilha Geral de Condominio":
    st.title("Planilha Geral de Condominio")

    with st.form("formulario_apartamento"):
        unidade = st.text_input("Unidade")
        vencimento_boleto = st.date_input("Vencimento do boleto")
        aluguel = st.number_input("Aluguel", min_value=0.0, format="%.2f")
        taxa_administracao_aluguel = st.number_input("Taxa de administração do aluguel", min_value=0.0, format="%.2f")
        data_inicio_contrato = st.date_input("Data de início do contrato")
        data_fim_contrato = st.date_input("Data de fim do contrato")
        valor_condominio = st.number_input("Valor do condomínio", min_value=0.0, format="%.2f")
        valor_agua = st.number_input("Valor da água", min_value=0.0, format="%.2f")
        valor_iptu = st.number_input("Valor do IPTU", min_value=0.0, format="%.2f")
        taxa_bancaria = st.number_input("Taxa bancária", min_value=0.0, format="%.2f")

        enviado = st.form_submit_button("Cadastrar")

        if enviado:
            # Inserir dados no banco de dados
            dados.inserir_dados(unidade, vencimento_boleto, aluguel, taxa_administracao_aluguel, data_inicio_contrato, data_fim_contrato, valor_condominio, valor_agua, valor_iptu, taxa_bancaria)
            st.success("Dados cadastrados com sucesso!")



# Página: Sobre o projeto
elif pagina == "Dados":
    st.title("Dados (Planilha Geral de Condominio)")
    dados = dados.listar_dados()
    df = pd.DataFrame(dados, columns=["ID", "Unidade", "Vencimento Boleto", "Aluguel", "Taxa de Administração Aluguel", "Data Início Contrato", "Data Fim Contrato", "Valor Condomínio", "Valor Água", "Valor IPTU", "Taxa Bancária"])
    st.dataframe(df)
    st.write("Total de registros:", len(df))
    st.write("Total de aluguel:", df["Aluguel"].sum())
    st.write("Total de taxa de administração:", df["Taxa de Administração Aluguel"].sum())
    st.write("Total de valor de condomínio:", df["Valor Condomínio"].sum())
    st.write("Total de valor de água:", df["Valor Água"].sum())
    st.write("Total de valor de IPTU:", df["Valor IPTU"].sum())
    st.write("Total de taxa bancária:", df["Taxa Bancária"].sum())
    st.write("Total de unidades:", df["Unidade"].nunique())
    st.write("Média de aluguel:", df["Aluguel"].mean())
    st.write("Média de taxa de administração:", df["Taxa de Administração Aluguel"].mean())
    st.write("Média de valor de condomínio:", df["Valor Condomínio"].mean())
    st.write("Média de valor de água:", df["Valor Água"].mean())
    st.write("Média de valor de IPTU:", df["Valor IPTU"].mean())
    st.write("Média de taxa bancária:", df["Taxa Bancária"].mean())
    st.write("Média de unidades:", df["Unidade"].nunique())
   


