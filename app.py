import os
from uuid import uuid4
from deepl import Translator

from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
from db import mongo, User
from bson import ObjectId

from auth.customer import blp as customer_blp
from auth.customer_rep import blp as rep_blp
from conversations.twilio_chat import blp as chat_blp


load_dotenv()

app = Flask(__name__)

# base flask config
app.config["MONGO_URI"] = "mongodb://localhost:27017/webchat"
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# initialise flask login
login_manager = LoginManager(app)

# initialise mongodb
mongo.init_app(app)

# authenticate deepl
translator = Translator(os.getenv("DEEPL_AUTH_KEY"))


# register blueprints
app.register_blueprint(customer_blp)
app.register_blueprint(rep_blp)
app.register_blueprint(chat_blp)


@login_manager.user_loader
def load_user(user_id):
    """fetch user id for login session"""
    user_data = mongo.db.customer.find_one(
        {"_id": ObjectId(user_id)}
    ) or mongo.db.customer_rep.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None


# set default login view for protected routes
login_manager.login_view = "customer.login"


@app.route("/")
def index():
    """return template for index page"""
    if current_user.is_anonymous:
        return render_template("index.html", user_id="anonymous")

    else:
        user = current_user.username
        id = str(uuid4())
        user_id = user + "-" + id

        return render_template("index.html", user_id=user_id)


@app.route("/translate", methods=["POST"])
def translate_text():
    """Translate chat with DEEPL client library"""
    request_data = request.get_json()
    input_text = request_data["text"]
    target_lang = request_data["target_lang"]

    response = translator.translate_text(text=input_text, target_lang=target_lang)

    response_text = response.text

    return jsonify({"response_text": response_text})
