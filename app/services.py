from .db import get_db

class EstoqueError(ValueError):
    pass

def listar_produtos():
    return get_db().execute("SELECT * FROM produtos WHERE ativo = 1 ORDER BY nome").fetchall()

def obter_produto(produto_id):
    return get_db().execute("SELECT * FROM produtos WHERE id_produto = ? AND ativo = 1", (produto_id,)).fetchone()

def cadastrar_produto(nome, categoria, preco, quantidade, minimo, validade=None):
    if not nome.strip() or not categoria.strip():
        raise EstoqueError("Nome e categoria são obrigatórios.")
    if preco < 0 or quantidade < 0 or minimo < 0:
        raise EstoqueError("Preço e quantidades não podem ser negativos.")
    db = get_db()
    db.execute("INSERT INTO produtos (nome,categoria,preco,quantidade_atual,estoque_minimo,data_validade) VALUES (?,?,?,?,?,?)", (nome.strip(), categoria.strip(), preco, quantidade, minimo, validade or None))
    db.commit()

def registrar_movimentacao(produto_id, tipo, quantidade, observacao=""):
    if tipo not in ("ENTRADA", "SAIDA"):
        raise EstoqueError("Tipo de movimentação inválido.")
    if quantidade <= 0:
        raise EstoqueError("A quantidade deve ser maior que zero.")
    db = get_db()
    produto = obter_produto(produto_id)
    if not produto:
        raise EstoqueError("Produto não encontrado.")
    novo_saldo = produto["quantidade_atual"] + quantidade if tipo == "ENTRADA" else produto["quantidade_atual"] - quantidade
    if novo_saldo < 0:
        raise EstoqueError(f"Quantidade maior que o estoque disponível. Informe até {produto['quantidade_atual']} unidades.")
    with db:
        db.execute("UPDATE produtos SET quantidade_atual = ? WHERE id_produto = ?", (novo_saldo, produto_id))
        db.execute("INSERT INTO movimentacoes (id_produto,tipo,quantidade,observacao) VALUES (?,?,?,?)", (produto_id, tipo, quantidade, observacao.strip()[:250]))
    return novo_saldo
