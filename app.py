import os

from flask import Flask, render_template, url_for
from jinja2 import TemplateNotFound
from routes import ROUTES

def create_app():
    print("Criando instância do aplicativo flask")
    app = Flask(__name__)

    for route in ROUTES:
        print(f"registrando a rota {route.name}")
        app.register_blueprint(route)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
