import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from swapproj.database import db_session
from swapproj.database import (
    User, Item, Message, Trade
)

bp = Blueprint('application', __name__, url_prefix='/')

@bp.route("/myItems", methods=["GET", "POST"])
def myItems():
    if request.method == "GET":
        return render_template("myItems.html")

@bp.route("/marketplace", methods=["GET", "POST"])
def marketplace():
    if request.method == "GET":
        return render_template("marketplace.html")

@bp.route("/createlisting", methods=["GET", "POST"])
def createlisting():
    if request.method == "GET":
        return render_template("listitem.html")