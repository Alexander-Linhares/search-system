import os

from flask import Flask, render_template, url_for
from blueprints import BLUEPRINTS_TO_REGISTER

def create_app():
    app = Flask(__name__)

    for bp in BLUEPRINTS_TO_REGISTER:
        app.register_blueprint(bp)

    @app.route('/')
    def root():
        return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
