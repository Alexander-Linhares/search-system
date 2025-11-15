import os

from flask import Flask, render_template, url_for
from jinja2 import TemplateNotFound
from blueprints import BLUEPRINTS_TO_REGISTER
from werkzeug.routing import Rule

def get_base_endpoint_from_blueprint(app, blueprint_name: str) -> str | None:
    for rule in app.url_map.iter_rules():
        rule: Rule
        if rule.endpoint.startswith(f'{blueprint_name}.'):
            if len(rule.arguments) <= 1:
                return rule.endpoint


def create_app():
    app = Flask(__name__)

    for bp in BLUEPRINTS_TO_REGISTER:
        app.register_blueprint(bp)

    base_endpoints = { 
        blueprint_name: get_base_endpoint_from_blueprint(app, blueprint_name)
        for blueprint_name in app.blueprints }
    
    print(base_endpoints)
    @app.route('/')
    def root():
        return render_template('index.j2', base_endpoints=base_endpoints)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
