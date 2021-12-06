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

@bp.route("/myitems", methods=["GET", "POST"])
def myItems():
    if request.method == "GET":
        return render_template("myItems.html")

@bp.route("/viewitems", methods=["GET", "POST"])
def viewitems():
    if request.method == "GET":
        return render_template("viewitems.html")

@bp.route("/listitem", methods=["GET", "POST"])
def listitem():
    if request.method == "GET":
        return render_template("listitem.html")
    else:
        title = request.form.get("title")
        description = request.form.get("description")
        img = request.form.get("filename")

        if not(title or description):
            flash("Please provide title and description")
            return redirect("/listitem")
        
        item = Item(
            name=title,
            description=description,
            img= img,
            timestamp= datetime.now(),
            sold=False,
            user_id= session["user_id"]
        )
        db_session.add(item)
        db_session.commit()

        flash("New listing created!")
        # Future TODO: redirect to /myitems
        return redirect("/")
