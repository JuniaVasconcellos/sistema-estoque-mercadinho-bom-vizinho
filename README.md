<img width="4032" height="1285" alt="image" src="https://github.com/user-attachments/assets/15d4dab0-b79c-437b-9f19-c87da2e49ad6" /># Sistema de Controle de Estoque do Mercadinho Bom Vizinho

MVP acadêmico de uma aplicação web responsiva para cadastrar produtos, registrar entradas e saídas, consultar saldos e destacar estoque baixo.

## Tecnologias
- Python 3.12
- Flask 3.1
- SQLite
- HTML5 e CSS3
- Pytest

## Executar localmente

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY="uma-chave-local-segura"
python run.py
```

Linux/macOS:
```bash
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="uma-chave-local-segura"
python run.py
```

Acesse `http://127.0.0.1:5000`.

## Testes
```bash
pytest -q
```

## Estrutura
- `app/routes.py`: rotas e coordenação do fluxo
- `app/services.py`: regras de negócio
- `app/db.py`: persistência SQLite
- `app/templates/`: telas Jinja
- `app/static/css/`: estilos responsivos e acessíveis
- `tests/`: testes automatizados

## Requisitos implementados
- RF01: cadastro de produtos
- RF02: entrada de estoque
- RF03: saída com bloqueio de saldo negativo
- RF04: consulta de saldos
- RF05: alerta de estoque baixo

## Observações de segurança
As consultas SQL são parametrizadas. A chave secreta deve ser fornecida por variável de ambiente. O modo debug fica desligado no arquivo de execução. Autenticação completa foi planejada, mas não foi incluída nesta versão mínima para não criar credenciais acadêmicas inseguras.

## Licença
Uso acadêmico.

## Auto-revisão técnica

A aplicação utiliza uma arquitetura monolítica modular, separando interface, regras de negócio e persistência. A revisão confirmou que as operações de entrada e saída são processadas em `services.py`, enquanto o acesso ao SQLite permanece concentrado em `db.py`.

As consultas ao banco utilizam parâmetros, reduzindo o risco de injeção de SQL. A regra de saída impede que o saldo fique negativo e produz uma mensagem compreensível para o usuário.

Como oportunidade de evolução, a aplicação deverá receber autenticação completa antes de uma implantação pública, além de proteção CSRF, HTTPS e controle individual de sessões.



