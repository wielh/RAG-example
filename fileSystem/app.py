from flask import Flask
from controller.knowledge_base import bp as knowledge_base_bp

def register_blueprints(app:Flask):
    app.register_blueprint(knowledge_base_bp)

if __name__ == '__main__':
    app = Flask(__name__)
    register_blueprints(app)
    app.run(debug=True)
