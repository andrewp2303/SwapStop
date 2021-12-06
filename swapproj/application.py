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

@bp.route("/listitem", methods=["GET", "POST"])
def listitem():
    if request.method == "GET":
        return render_template("listitem.html")
    else:
        title = request.form.get("title")
        description = request.form.get("description")
        img = request.files['file']
        print(img)
        filename = secure_filename(img.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in extensions:
                flash("Please use a correct file type")
                return redirect("/listitem")
            img.save(os.path.join(upload_path, filename))
        

        if not(title or description):
            flash("Please provide title and description")
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

# Finds the filename to display an image
@bp.route('/static/<filename>', methods = ["GET"])
def static(filename):
    return send_from_directory(upload_path, filename)
