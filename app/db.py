import sqlite3
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS produtos (
 id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
 nome TEXT NOT NULL UNIQUE,
 categoria TEXT NOT NULL,
 preco REAL NOT NULL CHECK(preco >= 0),
 quantidade_atual INTEGER NOT NULL DEFAULT 0 CHECK(quantidade_atual >= 0),
 estoque_minimo INTEGER NOT NULL DEFAULT 0 CHECK(estoque_minimo >= 0),
 data_validade TEXT,
 ativo INTEGER NOT NULL DEFAULT 1 CHECK(ativo IN (0,1))
);
CREATE TABLE IF NOT EXISTS movimentacoes (
 id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,
 id_produto INTEGER NOT NULL,
 tipo TEXT NOT NULL CHECK(tipo IN ('ENTRADA','SAIDA')),
 quantidade INTEGER NOT NULL CHECK(quantidade > 0),
 data_hora TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 observacao TEXT,
 FOREIGN KEY(id_produto) REFERENCES produtos(id_produto)
);
"""

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()

def seed_db():
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
    if total == 0:
        produtos = [
            ("Café 500 g", "Alimentos", 18.90, 8, 3, "2027-04-10"),
            ("Açúcar 1 kg", "Alimentos", 5.99, 2, 5, "2027-08-12"),
            ("Arroz 1 kg", "Alimentos", 7.50, 12, 5, "2027-09-15"),
            ("Óleo de Soja 900 ml", "Alimentos", 8.49, 4, 5, "2026-12-20"),
            ("Detergente 500 ml", "Limpeza", 2.99, 3, 5, None),
        ]
        db.executemany("INSERT INTO produtos (nome,categoria,preco,quantidade_atual,estoque_minimo,data_validade) VALUES (?,?,?,?,?,?)", produtos)
        db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)
