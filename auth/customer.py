from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mongo, User
from validations import LoginForm, SignupForm
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import WriteError

from flask_login import logout_user, login_user, login_required


blp = Blueprint("customer", __name__, url_prefix="/auth/customer")


@blp.route("/register", methods=["POST", "GET"])
def register():
    """Create customer account"""
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        username = request.form.get("username")
        language = request.form.get("language")
        password = request.form.get("password")

        password_hash = generate_password_hash(password)

        # check if username exists in database
        user = mongo.db.customer.find_one({"username": username})
        if user:
            flash("User already exists")
            return render_template("signup.html", form=form)

        try:
            mongo.db.customer.insert_one(
                {
                    "username": username,
                    "password": password_hash,
                    "language": language,
                    "role": "customer",
                    "chat_id": None,
                }
            )
            return redirect(url_for("customer.login"))

        except WriteError:
            flash("Error creating account.")
            return render_template("signup.html", form=form)

    return render_template("signup.html", form=form)


@blp.route("/login", methods=["POST", "GET"])
def login():
    """Login customer"""
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")

        user = mongo.db.customer.find_one({"username": username})

        if user and check_password_hash(user["password"], password):
            login_user(User(user))
            return redirect(url_for("index"))

        else:
            flash("Username/Password incorrect", "error")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@blp.route("/logout")
@login_required
def logout():
    """endpoint to clear current login session"""
    logout_user()
    return render_template("index.html")
