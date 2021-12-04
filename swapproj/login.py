import functools
import os
import requests
import urllib.parse

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
    # u = User('Bob', 'Jones', 'bob@gmail.com', 'user_bob', 'password')
    u = User(first_name='Bob', last_name='Jones', email='bob@gmail.com', username='user_bob', password='password')
    db_session.add(u)
    db_session.commit()

    print(User.query.all())
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # TODO
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    return render_template("register.html")