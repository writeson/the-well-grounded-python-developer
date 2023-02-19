import os
import yaml
from pathlib import Path
from flask import Flask, send_from_directory
from dynaconf import FlaskDynaconf
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import logging
import logging.config

login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"
flask_bcrypt = Bcrypt()
db = SQLAlchemy()


def create_app():
    """Initialize the Flask app instance"""

    # create the flask app instance
    app = Flask(__name__)
    dynaconf = FlaskDynaconf(extensions_list=True)

    with app.app_context():

        # create a route to the favicon.ico file
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(
                os.path.join(app.root_path, 'static'),
                'favicon.ico',
                mimetype="image/vnd.microsoft.icon"
            )

        # initialize plugins
        os.environ["ROOT_PATH_FOR_DYNACONF"] = app.root_path
        dynaconf.init_app(app)
        login_manager.init_app(app)
        flask_bcrypt.init_app(app)
        db.init_app(app)

        _configure_logging(app, dynaconf)

        # import the routes
        from . import intro
        from . import auth

        # register the blueprints
        app.register_blueprint(intro.intro_bp)
        app.register_blueprint(auth.auth_bp)

        # create the database if necessary
        db.create_all()

        return app


def _configure_logging(app, dynaconf):
    # configure logging
    logging_config_path = Path(app.root_path).parent / "logging_config.yaml"
    with open(logging_config_path, "r") as fh:
        logging_config = yaml.safe_load(fh.read())
        env_logging_level = dynaconf.settings.get("logging_level", "INFO").upper()
        logging_level = logging.INFO if env_logging_level == "INFO" else logging.DEBUG
        logging_config["handlers"]["console"]["level"] = logging_level
        logging_config["loggers"][""]["level"] = logging_level
        logging.config.dictConfig(logging_config)
