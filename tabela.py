import sqlite3
# Conectando ao banco de dados
conexao = sqlite3.connect('parque_tropical.db')

# Criando um cursor
cursor = conexao.cursor()

# Criando a tabela de apartamentos
cursor.execute('''
CREATE TABLE IF NOT EXISTS planilha_geral_condominio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contrato TEXT,
    unidade TEXT,
    vencimento_boleto DATE,
    aluguel REAL,
    taxa_administracao_aluguel REAL,
    data_inicio_contrato DATE,
    data_fim_contrato DATE,
    valor_condominio REAL,
    valor_agua REAL,
    valor_iptu REAL,
    taxa_bancaria REAL,
    nome_locatario TEXT,
    status_locacao BOOLEAN DEFAULT 0

               
               
)
''')

# FEchando a conexão
conexao.close()
print("Tabela 'planilha_geral_condominio' criada com sucesso!")