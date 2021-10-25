from flask import render_template

from monitor.view import view


@view.route("/", methods=["GET"])
def index():
    return render_template("index.html")