import functools
import os
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from swapproj.database import db_session
from swapproj.database import (
    Item, Message
)

bp = Blueprint('application', __name__, url_prefix='/', static_url_path='')
extensions = ['.jpg', '.png', '.gif', '.jpeg']
upload_path = 'swapproj/static/images'

# Route /myitems displays user listed/trade items
# GET: Retrieves and displays all items that are associated with the logged-in user
# POST: Displays information and messages pertaining to a specific item
@bp.route("/myitems", methods=["GET", "POST"])
def myitems():
    if request.method == "GET":

        # Retrieves user items
        items = db_session.query(Item).filter_by(user_id = session['user_id']).all()
        
        # Renders template that displays owned/previously owned items
        return render_template("myitems.html", items=items)
    else:
        # Retrieves messages and information on a specific item
        itemid = request.form.get("itemid")
        item = db_session.query(Item).filter_by(id = itemid).first()
        messages = []
        message = {}
        cmessages = db_session.execute("SELECT messages.text, messages.timestamp, users.username, users.email, users.first_name, users.last_name FROM users INNER JOIN messages ON users.id = messages.sender_id WHERE messages.item_id=:id",{'id':itemid})
        
        # Created a new list of dictionaries for messages in order to be able to access all desired values in correct formats
        for cmessage in cmessages:
            message["text"] = cmessage.text
            message["timestamp"] = datetime.strptime(cmessage.timestamp, '%Y-%m-%d %H:%M:%S.%f')
            message["username"] = cmessage.username
            message["email"] = cmessage.email
            message["name"] = cmessage.first_name + " " + cmessage.last_name
            messagecopy = message.copy()
            messages.append(messagecopy)
        return render_template("myitem.html",item=item, messages=messages)


# Route /myitem handles POST requests previously rendered myitem.html
# POST: Edit - loads a page that allows the user to edit selected listing
# POST: Cancel - Allows user to navigate back to their /myitems page
@bp.route("/myitem", methods=["POST"])
def myitem():
    if request.form.get("edit"):

        # Retrieves item information
        itemid = request.form.get("edit")
        item = db_session.query(Item).filter_by(id=itemid).first()

        # Displays UI to edit their listing
        return render_template("edit.html", item=item)
    else:

        # Redirects user back to their owned items page
        return redirect("/myitems")


# Route /edit only handles POST requests, either delete or update a listing
# POST: Update - Retrieves updated forms from edit.html and updates item in the databases
# POST: Delete - Deletes selected item and corresponding messages from database
@bp.route("/edit", methods=["POST"])
def edit():
    if request.form.get("update"):
        # Retrives changed listings from form
        itemid = request.form.get("update")
        citem = db_session.query(Item).filter_by(id=itemid).first()
        name = request.form.get("title")
        description = request.form.get("description")
        sold = True if request.form.get("sold") == "True" else False
        
        # initalizes the "updated item"
        item = {
            'name':name,
            'description':description,
            'img':citem.img,
            'datetime':citem.datetime,
            'sold':sold,
            'user_id':citem.user_id
        }

        # Updates listing in database
        db_session.query(Item).filter_by(id=itemid).update(item)
        db_session.commit()

        # Returns the user to up
        flash("Listing Updated")
        return redirect("/myitems")
    else:
        # Deletes messages and items database
        db_session.execute("DELETE FROM messages WHERE item_id =:id",{'id':request.form.get("delete")})
        db_session.execute("DELETE FROM items WHERE id =:id",{'id':request.form.get("delete")})
        db_session.commit()
        
        # Notifies user that there item was succesfully removed
        flash("Listing Deleted.")
        return redirect("/myitems")

# Route /viewitems handles both GET and POST request
# GET: Retrieves and displays from database every item that available and not owned by the user
# POST: Renders a specific items UI presenting with options if they want to contact the owner of the item
@bp.route("/viewitems", methods=["GET", "POST"])
def viewitems():
    if request.method == "GET":
        
        # Retrieve items that are to be displayed
        items = db_session.query(Item).filter_by(sold = False).filter(Item.user_id!=session["user_id"]).all()
        
        # Displays items
        return render_template("viewitems.html", items=items)
    else:

        # Retrieves selected item info
        itemid = request.form.get("itemid")
        item = db_session.query(Item).filter_by(id = itemid).first()

        # Displays select item
        return render_template("viewitem.html",item=item)


# Route /viewitem takes only POST requests
# POST: Contact -- allows the user to make an inquery about an item
# POST: Back -- allows the user to navigate back a page
@bp.route("/viewitem", methods=["POST"])
def viewitem():
    if request.form.get("contact"):
        itemid = request.form.get("contact")
        return render_template("contact.html", itemid=itemid)
    else:
        return redirect("/viewitems")

# Route /contact takes only POST requests and allows user to send messages
# POST: Message -- adds a message to the database and prompts user when the message is sent
@bp.route("/contact", methods=["POST"])
def contact():

    # Checks if the user provided a message
    if not request.form.get("description"):
        flash("Please provide a description!")
        itemid = request.form.get("itemid")
        return render_template("contact.html", itemid=itemid)
    else:
        # Initializes the new message
        itemid = request.form.get("itemid")
        item = db_session.query(Item).filter_by(id=itemid).first()
        message = Message(
            sender_id = session["user_id"],
            rec_id = item.user_id,
            timestamp = datetime.now(),
            text = request.form.get("description"),
            item_id = item.id
        )
        # Inserts into database
        db_session.add(message)
        db_session.commit()

        # Prompts user and redirects to "marketplace"
        flash("Message sent!")
        return redirect("/")

# Route /listitem takes both GET and POST requests
# GET: Displays form that allows user to and a listing
# POST: Creates Listing -- Retrieves information from forms and adds it to the database
@bp.route("/listitem", methods=["GET", "POST"])
def listitem():
    if request.method == "GET":
        return render_template("listitem.html")
    else:
        # Retrieves information from forms
        title = request.form.get("title")
        description = request.form.get("description")
        img = request.files['file']
        
        # Checks if all fields are filled
        if not(title or description or img):
            flash("Please provide title, description, and image")
            return redirect("/listitem")
        
        # Adds img to database or displays error
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

        # Initializes item
        item = Item(
            name=title,
            description=description,
            img=filename,
            datetime=datetime.now(),
            sold=False,
            user_id=session["user_id"]
        )

        # Adds initialized item to datadbase
        db_session.add(item)
        db_session.commit()

        # Prompts user and Redirects them to /myitems
        flash("New listing created!")
        return redirect("/myitems")

# Finds the filename to display an image
@bp.route('/static/<filename>', methods = ["GET"])
def static(filename):
    return send_from_directory(upload_path, filename)
