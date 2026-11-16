import os
from flask import Flask
from .db import init_app, init_db, seed_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.environ.get("DATABASE_PATH", os.path.join(app.instance_path, "estoque.db")),
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)
    init_app(app)
    from .routes import bp
    app.register_blueprint(bp)
    with app.app_context():
        init_db()
        seed_db()
    return app
