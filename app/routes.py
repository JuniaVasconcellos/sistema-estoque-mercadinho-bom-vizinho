from flask import Blueprint, flash, redirect, render_template, request, url_for
from .services import EstoqueError, cadastrar_produto, listar_produtos, obter_produto, registrar_movimentacao

bp = Blueprint("main", __name__)

@bp.get("/")
def index():
    produtos = listar_produtos()
    return render_template("index.html", total=len(produtos), alertas=sum(p["quantidade_atual"] <= p["estoque_minimo"] for p in produtos))

@bp.route("/produtos", methods=["GET", "POST"])
def produtos():
    if request.method == "POST":
        try:
            cadastrar_produto(request.form.get("nome", ""), request.form.get("categoria", ""), float(request.form.get("preco", 0)), int(request.form.get("quantidade", 0)), int(request.form.get("minimo", 0)), request.form.get("validade") or None)
            flash("Produto cadastrado com sucesso.", "success")
            return redirect(url_for("main.produtos"))
        except (ValueError, EstoqueError) as exc:
            flash(str(exc), "error")
    return render_template("produtos.html", produtos=listar_produtos())

@bp.route("/movimentar", methods=["GET", "POST"])
def movimentar():
    produtos = listar_produtos()
    if request.method == "POST":
        try:
            produto_id = int(request.form.get("produto_id", 0))
            produto = obter_produto(produto_id)
            novo = registrar_movimentacao(produto_id, request.form.get("tipo", ""), int(request.form.get("quantidade", 0)), request.form.get("observacao", ""))
            flash(f"Movimentação registrada com sucesso. Novo saldo de {produto['nome']}: {novo} unidades.", "success")
            return redirect(url_for("main.resultados"))
        except (ValueError, EstoqueError) as exc:
            flash(str(exc), "error")
    return render_template("movimentar.html", produtos=produtos)

@bp.get("/resultados")
def resultados():
    return render_template("resultados.html", produtos=listar_produtos())
