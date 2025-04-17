import sqlite3

# Conectando ao banco de dados
conexao = sqlite3.connect('parque_tropical.db')
cursor = conexao.cursor() 


# atualiza dados
cursor.execute('''
UPDATE apartamentos
SET
    preco = 1300.00,
    descricao = 'Apartamento com vista para o parque e varanda oi',
    aluguel = 0.0,
    satus_aluguel = 1
WHERE
    id = 1
''')

conexao.commit()
print("Dados atualizados com sucesso!")