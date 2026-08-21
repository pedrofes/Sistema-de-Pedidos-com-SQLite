import sqlite3

conexao = sqlite3.connect('estoque.db')

cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE clientes(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nome TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE
);
''')


cursor.execute('''
CREATE TABLE produtos(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nome TEXT NOT NULL,
	preco REAL NOT NULL,
	estoque INTEGER NOT NULL

);
''')

cursor.execute('''
CREATE TABLE pedidos(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	cliente_id INTEGER NOT NULL,
	produto_id INTEGER NOT NULL,
	quantidade INTEGER NOT NULL,
	FOREIGN KEY (cliente_id) REFERENCES clientes(id),
	FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
''')


conexao.commit()

conexao.close()