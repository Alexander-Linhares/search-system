import os

from flask import Flask, render_template, url_for
from jinja2 import TemplateNotFound
from app.routes import ROUTES

def create_app():
    print("Criando instância do aplicativo flask")
    app = Flask(__name__)

    app.config.from_pyfile('./config.py')

    for route in ROUTES:
        print(f"registrando a rota {route.name}")
        app.register_blueprint(route)
    
    return app

app = create_app()