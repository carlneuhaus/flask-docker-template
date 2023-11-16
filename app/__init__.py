from flask import Flask

def create_app():

    app = Flask(__name__)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=8090)