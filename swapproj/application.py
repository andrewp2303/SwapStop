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
def createlisting():
    if request.method == "GET":
        return render_template("listitem.html")

@bp.route("/viewitem", methods=["GET","POST"])
def viewitem():
    if request.method == "GET":
        # item = db_session.execute("SELECT * FROM items WHERE id = :id",{'id':session["item_id"]}).first()
        item = {'description': "coolapp", 'sold':"No",'timestamp':"22/02/2021"}
        return render_template("viewitem.html", item=item)
    else:
        if request.form.get("proposetrade"):
            # TODO: Proposes trade
            return "Not implemented"
        elif request.form.get("contact"):
            # TODO: Displays contact information
            return "Not implemented"
        else:

            return redirect("/viewitems")


# @bp.route("/contact", methods=["GET"])
# def contact():
#     ownerinfo = db_session.execute("SELECT * FROM users WHERE id IN (SELECT user_id FROM items WHERE item.id = :id)",{'id':session["item_id"]})
#     return render_template("viewcontactinfo.html", info=ownerinfo)
