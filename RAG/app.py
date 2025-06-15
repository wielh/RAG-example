from flask import Flask
from controller.ask import bp as ask_bp

def register_blueprints(app:Flask):
    app.register_blueprint(ask_bp)

if __name__ == '__main__':
    app = Flask(__name__)
    register_blueprints(app)
    app.run(debug=True, port=5001)
