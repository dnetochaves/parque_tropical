import sqlite3

# Conectando ao banco de dados
conexao = sqlite3.connect('parque_tropical.db')
cursor = conexao.cursor() 

# Lendo dados da tabela apartamentos
cursor.execute('''
SELECT * FROM apartamentos
''')
# Lendo todos os resultados
apartamentos = cursor.fetchall()
# Fechando a conexão
conexao.close()
print("Dados lidos com sucesso!")   
print(apartamentos)