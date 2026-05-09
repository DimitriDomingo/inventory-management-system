from flask import Flask, request, jsonify
from database import conectar

app = Flask(__name__)

@app.route("/")
def home():
    return "A API está rodando!"

@app.route("/produtos", methods = ["POST"])
def criar_produto():

    dados = request.json

    nome_produto = dados["nome"]
    valor = dados["valor"]
    estoque = dados["estoque"]

    conn, cursor = conectar()

    cursor.execute("""
        INSERT INTO produtos (nome_produto, valor, estoque) VALUES (?, ?, ?)
""", (nome_produto, valor, estoque,))
    
    conn.commit()
    conn.close()

    return {"Mensagem": "Produto criado com sucesso!"}
    
@app.route("/produtos", methods = ["GET"])
def listar_produtos():
    conn, cursor = conectar()
    cursor.execute("""
        SELECT * FROM produtos
""")
    
    dados = cursor.fetchall()
    produtos = []

    for produto in dados:
         produtos.append({"Nome": produto[0],
                        "Valor": produto[1],
                        "Estoque": produto[2]})
    
    conn.close()

    return jsonify(produtos)
    
@app.route("/produtos/<int:id>", methods = ["GET"])
def produto_por_id(id):
    conn, cursor = conectar()
    cursor.execute("""
        SELECT * FROM produtos WHERE id = ?
""", (id,))
    
    dados = cursor.fetchone()

    if not dados:
        conn.close()
        return {"Mensagem": "Produto não encontrado!"}
    
    conn.close()

    return {"Nome": dados[0],
            "Valor": dados[1],
            "Estoque": dados[2]}

@app.route("/produtos/<int:id>", methods = ["PUT"])
def atualizar_produto(id):
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
        

@app.route("/produtos/<int:id>", methods = ["DELETE"])
def deletar_produto(id):
    conn, cursor = conectar()

    cursor.execute("""SELECT * FROM produtos WHERE id = ?""", (id,))
    dados = cursor.fetchone()

    if not dados:
        conn.close()
        return {"Mensagem": "Produto não encontrado!"}
    
    else:
        cursor.execute("""
            DELETE FROM produtos WHERE id = ?
    """, (id,))
        
        conn.commit()
        conn.close()