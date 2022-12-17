from flask import Flask, render_template
from datetime import datetime
from random import sample


class PageVisit:
    COUNT = 0

    def counts(self):
        PageVisit.COUNT += 1
        return PageVisit.COUNT


class BannerColors:
    COLORS = [
        "lightcoral", "salmon", "red", "firebrick", "pink",
        "gold", "yellow", "khaki", "darkkhaki", "violet",
        "blue", "purple", "indigo", "greenyellow", "lime",
        "green", "olive", "darkcyan", "aqua", "skyblue",
        "tan", "sienna", "gray", "silver"
    ]

    def get_colors(self):
        return sample(BannerColors.COLORS, 5)


def create_app():
    """Initialize the Flask app instance"""

    app = Flask(__name__)

    with app.app_context():

        @app.route("/")
        def home():
            return render_template("index.html", data={
                "now": datetime.now(),
                "page_visit": PageVisit(),
                "banner_colors": BannerColors().get_colors()
            })

        return app
