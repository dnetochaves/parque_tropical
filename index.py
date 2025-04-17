import streamlit as st
import dados
import pandas as pd
import numpy as np
import random
import sqlite3
# Configurações da página
st.set_page_config(page_title="Gestão de Apartamentos", layout="wide", initial_sidebar_state="expanded")

# Menu lateral
st.sidebar.title("Menu")
pagina = st.sidebar.radio("Navegação", ["Planilha Geral de Condominio", "Add Contrato", "Excluir Contrato"])

# Página: Cadastro
if pagina == "Planilha Geral de Condominio":
    st.title("Dados (Planilha Geral de Condominio)")

    
    
    dados = dados.listar_dados()
    

    



    df = pd.DataFrame(dados, columns=["ID", "Contrato", "Unidade", "Vencimento Boleto", "Aluguel", "Taxa de Administração Aluguel", "Data Início Contrato", "Data Fim Contrato", "Valor Condomínio", "Valor Água", "Valor IPTU", "Taxa Bancária", "Nome Locatario"])
    st.dataframe(df)
    
    st.divider()
    
        # --- Totais ---
    st.subheader("🔢 Totais")
    totais = {
        "Total de registros": len(df),
        "Total de aluguel": df["Aluguel"].sum(),
        "Total de taxa de administração": df["Taxa de Administração Aluguel"].sum(),
        "Total de condomínio": df["Valor Condomínio"].sum(),
        "Total de água": df["Valor Água"].sum(),
        "Total de IPTU": df["Valor IPTU"].sum(),
        "Total de taxa bancária": df["Taxa Bancária"].sum(),
        "Total de unidades": df["Unidade"].nunique()
    }

    cols = st.columns(4)
    for i, (label, valor) in enumerate(totais.items()):
        cols[i % 4].metric(label, f"R$ {valor:,.2f}" if isinstance(valor, (int, float)) and "Total de registros" not in label and "unidades" not in label.lower() else valor)

    st.divider()
    # --- Médias ---
    st.subheader("📈 Médias")
    medias = {
        "Média de aluguel": df["Aluguel"].mean(),
        "Média de taxa de administração": df["Taxa de Administração Aluguel"].mean(),
        "Média de condomínio": df["Valor Condomínio"].mean(),
        "Média de água": df["Valor Água"].mean(),
        "Média de IPTU": df["Valor IPTU"].mean(),
        "Média de taxa bancária": df["Taxa Bancária"].mean()
    }

    cols2 = st.columns(3)
    for i, (label, valor) in enumerate(medias.items()):
        cols2[i % 3].metric(label, f"R$ {valor:,.2f}")



# Página: Sobre o projeto
elif pagina == "Add Contrato":
    st.title("Cadastrar Contrato")

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
        nome_locatario = st.text_input("Nome Locatário")

        enviado = st.form_submit_button("Cadastrar")

        if enviado:
            # Inserir dados no banco de dados
            contrato = random.randint(1000, 9999)  # Gerar um número aleatório para o contrato
            dados.inserir_dados(contrato, unidade, vencimento_boleto, aluguel, taxa_administracao_aluguel, data_inicio_contrato, data_fim_contrato, valor_condominio, valor_agua, valor_iptu, taxa_bancaria, nome_locatario)
            st.success("Dados cadastrados com sucesso!")



    
elif pagina == "Excluir Contrato":
    st.title("Excluir Contrato")
    numero_contrato = st.text_input("Digite o CONTRATO a ser excluído:")
    if st.button("Confirmar Exclusão"):
            if numero_contrato.strip():  # Verifica se não está vazio ou só espaços
                try:
                    conexao = sqlite3.connect('parque_tropical.db')
                    cursor = conexao.cursor()

                    # Verifica se o contrato existe antes de excluir
                    cursor.execute('SELECT * FROM planilha_geral_condominio WHERE contrato = ?', (numero_contrato,))
                    registro = cursor.fetchone()

                    if registro:
                        cursor.execute('DELETE FROM planilha_geral_condominio WHERE contrato = ?', (numero_contrato,))
                        conexao.commit()
                        st.success(f"Registro com CONTRATO {numero_contrato} excluído com sucesso!")
                        
                    else:
                        st.warning(f"Nenhum registro encontrado com CONTRATO {numero_contrato}. Nenhuma exclusão realizada.")
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao tentar excluir: {e}")
                finally:
                    conexao.close()
                    st.session_state.mostrar_confirmacao = False
            else:
                st.warning("Por favor, insira um número de contrato válido.")


