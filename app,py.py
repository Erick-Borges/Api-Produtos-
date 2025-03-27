from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario_api:@localhost/minha_api'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Tabela "produtos"
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    fornecedor = db.Column(db.String(100), nullable=False)
    endereco_fornecedor = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

# Criar a tabela no banco de dados
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({'mensagem': 'API de Produtos funcionando!'})

if __name__ == '__main__':
    app.run(debug=True)


# Criar um novo produto (POST)
@app.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.json
    novo_produto = Produto(
        nome=dados['nome'],
        fornecedor=dados['fornecedor'],
        endereco_fornecedor=dados['endereco_fornecedor'],
        quantidade=dados['quantidade'],
        endereco=dados['endereco'],
        preco_unitario=dados['preco_unitario']
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto criado com sucesso!'}), 201


# Listar todos os produtos (GET)
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    resultado = [{'id': p.id, 'nome': p.nome, 'quantidade': p.quantidade} for p in produtos]
    return jsonify(resultado)

# Atualizar um produto pelo ID (PUT)
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    dados = request.json
    produto.nome = dados.get('nome', produto.nome)
    produto.quantidade = dados.get('quantidade', produto.quantidade)
    db.session.commit()
    return jsonify({'mensagem': 'Produto atualizado com sucesso!'})

# Deletar um produto pelo ID (DELETE)
@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto deletado com sucesso!'})

