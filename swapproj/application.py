import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from swapproj.database import db_session
from swapproj.database import (
    User, Item, Message, Trade
)

bp = Blueprint('application', __name__, url_prefix='/', static_url_path='')
extensions = ['.jpg', '.png', '.gif', '.jpeg']
upload_path = 'swapproj/static/images'

@bp.route("/myitems", methods=["GET", "POST"])
def myitems():
    if request.method == "GET":
        items = db_session.query(Item).filter_by(user_id = session['user_id']).all()
        return render_template("myitems.html", items=items)


@bp.route("/viewitems", methods=["GET", "POST"])
def viewitems():
    if request.method == "GET":
        items = db_session.query(Item).all()
        return render_template("viewitems.html", items=items)
    else:
        item_id = request.form.get("id")
        #item = db_session.execute("SELECT * FROM items WHERE id = :id",{'id':id}).first()
        item = db_session.query(Item).filter_by(id = item_id).first()
        #item = {'description': "coolapp", 'sold':"No",'timestamp':"22/02/2021"}
        return "" + str(request.form.get("id"))

@bp.route("/listitem", methods=["GET", "POST"])
def listitem():
    if request.method == "GET":
        return render_template("listitem.html")
    else:
        title = request.form.get("title")
        description = request.form.get("description")
        img = request.files['file']
        
        if not(title or description or img):
            flash("Please provide title, description, and image")
            return redirect("/listitem")

        filename = secure_filename(img.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in extensions:
                flash("Please use a correct file type")
                return redirect("/listitem")
            img.save(os.path.join(upload_path, filename))
        else:
            flash("Please provide an image")
            return redirect("/listitem")

        item = Item(
            name=title,
            description=description,
            img=filename,
            datetime=datetime.now(),
            sold=False,
            user_id=session["user_id"]
        )
        db_session.add(item)
        db_session.commit()

        flash("New listing created!")
        # Future TODO: redirect to /myitems
        return redirect("/")

@bp.route("/viewitem", methods=["GET","POST"])
def viewitem():
    if request.method == "GET":
        item_id = request.form.get("id")
        #item = db_session.execute("SELECT * FROM items WHERE id = :id",{'id':id}).first()
        item = db_session.query(Item).filter_by(id = item_id).first()
        #item = {'description': "coolapp", 'sold':"No",'timestamp':"22/02/2021"}
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


# Finds the filename to display an image
@bp.route('/static/<filename>', methods = ["GET"])
def static(filename):
    return send_from_directory(upload_path, filename)
