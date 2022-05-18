from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sgsdvsdfas'

    from main.routes import main
    from errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
