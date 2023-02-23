import logging
import logging.config
import os
from datetime import timezone
from pathlib import Path

import pytz
import yaml
from dynaconf import FlaskDynaconf
from flask import Flask, send_from_directory, session
from flask.templating import render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown

login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"
flask_bcrypt = Bcrypt()
db = SQLAlchemy()
pagedown = PageDown()
markdown = None


def create_app():
    """Initialize the Flask app instance"""

    # create the flask app instance
    app = Flask(__name__)
    dynaconf = FlaskDynaconf(extensions_list=True)

    with app.app_context():

        # create a route to the favicon.ico file
        @app.route("/favicon.ico")
        def favicon():
            return send_from_directory(
                os.path.join(app.root_path, "static"),
                "favicon.ico",
                mimetype="image/vnd.microsoft.icon",
            )

        # initialize plugins
        os.environ["ROOT_PATH_FOR_DYNACONF"] = app.root_path
        dynaconf.init_app(app)
        login_manager.init_app(app)
        flask_bcrypt.init_app(app)
        db.init_app(app)
        pagedown.init_app(app)
        Markdown(app)
        _configure_logging(app, dynaconf)

        # import the routes
        from . import auth, content, intro

        # register the blueprints
        app.register_blueprint(intro.intro_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(content.content_bp)

        # create the database if necessary
        db.create_all()

        # initialize the role table
        from .models import Role

        Role.initialize_role_table()

        # register error handlers
        app.register_error_handler(403, error_page)
        app.register_error_handler(404, error_page)
        app.register_error_handler(500, error_page)

        # inject the role permissions class into all template contexts
        @app.context_processor
        def inject_permissions():
            return dict(Permissions=Role.Permissions)

        @app.template_filter()
        def format_datetime(value, format="%Y-%m-%d %H:%M:%S"):
            value_with_timezone = value.replace(tzinfo=timezone.utc)
            tz = pytz.timezone(
                session.get("timezone_info", {}).get("timeZone", "US/Eastern")
            )
            local_now = value_with_timezone.astimezone(tz)
            return local_now.strftime(format)

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


def error_page(e):
    return render_template("error.html", e=e), e.code
