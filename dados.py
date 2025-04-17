import sqlite3

# Conectando ao banco de dados
def conecta_bd():
    conexao = sqlite3.connect('parque_tropical.db')
    return conexao

# Inserir dados
def inserir_dados(unidade, vencimento_boleto, aluguel, taxa_administracao_aluguel, data_inicio_contrato, data_fim_contrato, valor_condominio, valor_agua, valor_iptu, taxa_bancaria):
    conexao = conecta_bd()
    cursor = conexao.cursor()

    cursor.execute('''
    INSERT INTO planilha_geral_condominio (unidade, vencimento_boleto, aluguel, taxa_administracao_aluguel, data_inicio_contrato, data_fim_contrato, valor_condominio, valor_agua, valor_iptu, taxa_bancaria)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (unidade, vencimento_boleto, aluguel, taxa_administracao_aluguel, data_inicio_contrato, data_fim_contrato, valor_condominio, valor_agua, valor_iptu, taxa_bancaria))
    conexao.commit()
    conexao.close()

#Listagem de dados
def listar_dados():
    conexao = conecta_bd()
    cursor = conexao.cursor()
    
    cursor.execute('SELECT * FROM planilha_geral_condominio')
    dados = cursor.fetchall()
    
    conexao.close()
    return dados