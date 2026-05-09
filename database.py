import sqlite3

def conectar():
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()

def criar_tabela():
    conn, cursor = conectar()
    cursor.execuete("""
        CREATE TABLE IF NOT EXISTS produtos
        ( id_produto INTEGER PRIMARY KEY,
        nome_produto TEXT NOT NULL,
        valor REAL,
        estoque INTEGER NOT NULL)
""")