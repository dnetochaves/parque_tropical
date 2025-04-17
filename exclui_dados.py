import sqlite3

# Conectando ao banco de dados
conexao = sqlite3.connect('parque_tropical.db')
cursor = conexao.cursor() 

#excluir dadis da tabela apartamento
cursor.execute('''
DELETE FROM apartamentos
WHERE id = 3
''')
# Commitando as alterações
conexao.commit()
# Fechando a conexão
conexao.close()
print("Dados excluídos com sucesso!")