import os
import sys

import pytest
from flask_sqlalchemy import SQLAlchemy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
_original_init_app = SQLAlchemy.init_app


def _init_app_in_memory(self, app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    _original_init_app(self, app)


SQLAlchemy.init_app = _init_app_in_memory
try:
    from project import app as flask_app, db
finally:
    SQLAlchemy.init_app = _original_init_app


@pytest.fixture
def app():
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    with flask_app.app_context():
        db.create_all()

    yield flask_app

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
