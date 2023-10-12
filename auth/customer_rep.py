from flask import Blueprint, request, render_template, redirect, flash, url_for
from db import mongo, User
from validations import LoginForm

from flask_login import login_user, logout_user


blp = Blueprint("rep", __name__, url_prefix="/auth/rep")


@blp.route("/login", methods=["POST", "GET"])
def login():
    """Login customer rep"""
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")

        customer_reps = mongo.db.customer_rep.find_one({"username": username})

        if customer_reps and customer_reps["password"] == password:
            login_user(User(customer_reps))

            users = mongo.db.customer.find()
            context = {"conversations": []}

            for user in users:
                context["conversations"].append(
                    {"username": user["username"], "chat_id": user["chat_id"]}
                )

            return render_template("repchats.html", context=context)

        else:
            flash("username/password incorrect")
            return render_template("rep_login.html", form=form)

    return render_template("rep_login.html", form=form)


@blp.route("logout")
def logout():
    """Log out user"""
    logout_user()
    return redirect(url_for("index"))
