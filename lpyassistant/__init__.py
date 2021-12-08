__version__ = '0.1.0'


from flask import Flask
import secrets
def create_app():
    app = Flask(__name__)
    app.debug = True
    secret_key = secrets.token_bytes(32)
    app.config['SECRET_KEY'] = secret_key

    with app.app_context():
        import lpyassistant.flask

        return app
