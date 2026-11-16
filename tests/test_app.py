import os, tempfile
import pytest
from app import create_app
from app.services import registrar_movimentacao, EstoqueError

@pytest.fixture
def app():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    app = create_app({"TESTING": True, "DATABASE": path, "SECRET_KEY": "test"})
    yield app
    os.unlink(path)

def test_home(app):
    client = app.test_client()
    assert client.get("/").status_code == 200

def test_saida_valida(app):
    with app.app_context():
        assert registrar_movimentacao(1, "SAIDA", 3) == 5

def test_bloqueia_saldo_negativo(app):
    with app.app_context():
        with pytest.raises(EstoqueError):
            registrar_movimentacao(1, "SAIDA", 99)
