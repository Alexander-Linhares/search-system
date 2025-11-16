import os

from flask import Flask, render_template, url_for
from jinja2 import TemplateNotFound
from blueprints import BLUEPRINTS_TO_REGISTER
from werkzeug.routing import Rule

def get_base_endpoint_from_blueprint(app, blueprint_name: str) -> str | None:
    """
        Encontra o endpoint (ex: 'logs.logs_handler') da rota base de uma Blueprint.
    """
    for rule in app.url_map.iter_rules():
        rule: Rule
        if rule.endpoint.startswith(f'{blueprint_name}.'):
            if len(rule.arguments) <= 1:
                return rule.endpoint


def create_app():
    print("Criando instância do aplicativo flask")
    app = Flask(__name__)

    print("adicionando blueprints")
    for bp in BLUEPRINTS_TO_REGISTER:
        print(f'Adicionando: {bp}')
        app.register_blueprint(bp)

    print("Tratando endereçamento dos endpoints")
    #Associa o nome da blueprint com a função registrada para a rota, isso é importante para o mapeamento dinâmico de url_for
    base_endpoints = { 
        blueprint_name: get_base_endpoint_from_blueprint(app, blueprint_name)
        for blueprint_name in app.blueprints }
    
    print("endpoins:")
    print(base_endpoints)

    print("inicializando rota raiz")
    @app.route('/')
    def root():
        return render_template('index.j2', base_endpoints=base_endpoints)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
