# Framework flask
from flask import Flask

# Blueprint
from .views.routes import main

# Criação do app flask com blueprint
def create_app():
    app = Flask(__name__)

    app.register_blueprint(main)

    return app

