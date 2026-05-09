from flask import Flask, request
from database import conectar

app = Flask(__name__)

@app.route("/")
def home():
    return "A API está rodando!"

@app.route("/produtos", methods = ["POST"])
def criar_produto(nome_produto, valor, estoque):
    conn, cursor = conectar()
    cursor.execute("""
        INSERT INTO produtos VALUES (nome, valor, estoque), (?, ?, ?)
""", (nome_produto, valor, estoque,))
    
    conn.commit()
    conn.close()
    
@app.route("/produtos", methods = ["GET"])
def listar_produtos():
    conn, cursor = conectar()
    cursor.execute("""
        SELECT * FROM produtos
""")
    
    dados = cursor.fetchall()

    for produto in dados:
        return {"Nome": produto[0],
                "Valor": produto[1],
                "Estoque": produto[2]}
    
    conn.close()
    
@app.route("/produtos/<int:id>", methods = ["GET"])
def produto_por_id(id):
    conn, cursor = conectar()
    cursor.executar("""
        SELECT * FROM produtos WHERE id = ?
""", (id,))
    
    dados = cursor.fetchone()

    for produto in dados:
        return {"Nome": produto[0],
                "Valor": produto[1],
                "Estoque": produto[2]}
    
    conn.close()

@app.route("/produtos/<int:id>", methods = ["PUT"])
def atualizar_produto(id, estoque):
    conn, cursor = conectar()
    dados = request.json
    estoque = dados["estoque"]
    
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()

    if not produto:
        conn.close()
        return{"Mensagem": "Produto inexistente"}
        
    if estoque < 0:
        conn.close()
        return {"Mensagem": "Estoque não pode ser negativo"}
    
    cursor.execute("""UPDATE produtos SET estoque = ? WHERE id = ?""", (estoque, id))

    conn.commit()
    conn.close()

    return {"Mensagem": "Protudo atualizado com sucesso"}
        

@app.route("/produtos", methods = ["DELETE"])
def deletar_produto(id):
    conn, cursor = conectar()
    cursor.execute("""
        DELETE * FROM produtos WHERE id = ?
""", (id))