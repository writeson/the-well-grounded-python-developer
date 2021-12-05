from flask import Flask


def create_app():
    """Initialize the Flask app instance"""

    app = Flask(__name__)

    with app.app_context():

        # import the routes
        from . import intro

        # register the blueprints
        app.register_blueprint(intro.intro_bp)

        return app
