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
    else:
        itemid = request.form.get("itemid")
        item = db_session.query(Item).filter_by(id = itemid).first()
        # messages = db_session.query(Message).filter_by(item_id = itemid).all()
        # TODO: Fix displayed time
        # messages = db_session.query(Message).join(User, Message.sender_id == User.id).filter_by(item_id = itemid).all()
        # messages = db_session.query(messages).filter_by(item_id = itemid).all
        messages = []
        message = {}
        cmessages = db_session.execute("SELECT messages.text, messages.timestamp, users.username, users.email, users.first_name, users.last_name FROM users INNER JOIN messages ON users.id = messages.sender_id WHERE messages.item_id=:id",{'id':itemid})
        for cmessage in cmessages:
            message["text"] = cmessage.text
            message["timestamp"] = datetime.strptime(cmessage.timestamp, '%Y-%m-%d %H:%M:%S.%f')
            message["username"] = cmessage.username
            message["email"] = cmessage.email
            message["name"] = cmessage.first_name + " " + cmessage.last_name
            messagecopy = message.copy()
            messages.append(messagecopy)
        return render_template("myitem.html",item=item, messages=messages)

@bp.route("/myitem", methods=["POST"])
def myitem():
    if request.form.get("edit"):
        itemid = request.form.get("edit")
        item = db_session.query(Item).filter_by(id=itemid).first()
        return render_template("edit.html", item=item)
    else:
        return redirect("/myitems")



@bp.route("/edit", methods=["POST"])
def edit():
    if request.form.get("update"):
        itemid = request.form.get("update")
        name = request.form.get("title")
        description = request.form.get("description")
        sold = True if request.form.get("sold") == "True" else False
        if not name or not description:
            flash("Please enter a name and description!")
            item = db_session.query(Item).filter_by(id=itemid).first()
            return render_template("edit.html", item=item)

        updateditem = {
            "name": name,
            "description": description,
            "sold": sold
        }

        db_session.query(Item).filter_by(id=itemid).update(updateditem)
        db_session.commit()

        flash("Item updated!")
        return redirect("/myitems")
    else:
        itemid = request.form.get("delete")
        db_session.query(Item).filter_by(id=itemid).delete()
        db_session.commit()
        flash("Item deleted!")
        return redirect("/myitems")


@bp.route("/viewitems", methods=["GET", "POST"])
def viewitems():
    if request.method == "GET":
        items = db_session.query(Item).filter_by(sold = False).all()
        return render_template("viewitems.html", items=items)
    else:
        itemid = request.form.get("itemid")
        item = db_session.query(Item).filter_by(id = itemid).first()
        return render_template("viewitem.html",item=item)


@bp.route("/viewitem", methods=["POST"])
def viewitem():
    if request.form.get("contact"):
        itemid = request.form.get("contact")
        #item = db_session.query(Item).filter_by(id=item_id).first()
        return render_template("contact.html", itemid=itemid)
    else:
        return redirect("/viewitems")

@bp.route("/contact", methods=["POST"])
def contact():


    if not request.form.get("description"):
        flash("Please provide a description!")
        itemid = request.form.get("itemid")
        return render_template("contact.html", itemid=itemid)
    else:
        itemid = request.form.get("itemid")
        item = db_session.query(Item).filter_by(id=itemid).first()
        message = Message(
            sender_id = session["user_id"],
            rec_id = item.user_id,
            timestamp = datetime.now(),
            text = request.form.get("description"),
            item_id = item.id
        )
        db_session.add(message)
        db_session.commit()
        flash("Message sent!")
        return redirect("/")


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

# Finds the filename to display an image
@bp.route('/static/<filename>', methods = ["GET"])
def static(filename):
    return send_from_directory(upload_path, filename)
