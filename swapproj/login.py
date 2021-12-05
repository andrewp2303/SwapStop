import functools
import os
import requests
import urllib.parse
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from swapproj.database import db_session
from .database import User
from functools import wraps

bp = Blueprint('login', __name__, url_prefix='/')

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")
   
    # User reached route via POST (as by submitting a form via POST)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            flash("Password and username required.")
            return redirect("/login")

        rows = db_session.execute("SELECT * FROM users WHERE username = :u",{'u':username}).first()

        if not rows or not check_password_hash(rows["password"],password):
            flash("Incorrect password or username.")
            return redirect("/login")

        session["user_id"] = rows["id"]

        return redirect("/")
   
@bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")
    
    else:
        # TODO: add get() field after html templates are complete
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword =request.form.get("confirmation")

        if not(firstname and lastname and email and password and confirmpassword):
            flash("All fields must be filled.")
            return redirect("/register")

        rows = db_session.execute("SELECT * FROM users WHERE username = :u",{'u':username}).first()
        
        if rows:
            flash("Username taken.")
            return redirect("/register")

        if password != confirmpassword:
            flash("Password do not match.")
            return redirect("/register")

        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Please enter a valid email.")
            return redirect("/register")

        u = User(first_name=firstname, last_name=lastname, email=email,username=username, password=generate_password_hash(password))
        db_session.add(u)
        db_session.commit()

        flash("New account created! Please login.")
        return redirect("/login")
        
