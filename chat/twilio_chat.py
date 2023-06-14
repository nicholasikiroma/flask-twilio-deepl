import os

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from flask_login import login_required
from flask import Blueprint, render_template
from flask_login import current_user
from bson import ObjectId


blp = Blueprint("chat", __name__, url_prefix="/chat")


account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)


def generate_access_token(identity, service_sid):
    """Generates access token
    Args:
         identity - identity of conversation participant
         service_sid - unique ID of the Conversation Service
    Return:
         jwt encoded access token
    """
    twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_api_key_sid = os.environ.get("TWILIO_API_KEY_SID")
    twilio_api_key_secret = os.environ.get("TWILIO_API_KEY_SECRET")

    token = AccessToken(
        twilio_account_sid,
        twilio_api_key_sid,
        twilio_api_key_secret,
        identity=identity,
    )

    token.add_grant(ChatGrant(service_sid=service_sid))

    return token.to_jwt()


@blp.route("/<string:user_id>")
@login_required
def conversation(user_id):
    """Create Twilio conversation"""
    # check if user exists
    # if user is active check there is an existing conversation
    # if yes, retrieve conversation
    if current_user.is_active and current_user.chat_id:
        chat_id = current_user.chat_id

        conversation = client.conversations.v1.conversations(chat_id).fetch()

        # generate an access token
        service_sid = conversation.chat_service_sid

        token = generate_access_token(current_user.username, service_sid)

        context = {
            "token": token,
            "chat_id": conversation.sid,
            "role": current_user.role,
            "language": current_user.language,
        }

        return render_template("chat.html", context=context)

    elif current_user.is_authenticated and current_user.chat_id == None:
        # create conversation
        try:
            conversation = client.conversations.v1.conversations.create(
                friendly_name=user_id
            )
        except TwilioException as err:
            print("Error:", err)

        user = current_user.id
        from db import mongo

        # add chat_id for current user to database
        mongo.db.customer.update_one(
            {"_id": ObjectId(user)}, {"$set": {"chat_id": conversation.sid}}
        )

        try:
            # add current user to conversation
            client.conversations.v1.conversations(conversation.sid).participants.create(
                identity=current_user.username
            )
        except TwilioException as err:
            print("Error:", err)

        # generate an access token
        service_sid = conversation.chat_service_sid

        token = generate_access_token(current_user.username, service_sid)

        context = {
            "token": token,
            "chat_id": conversation.sid,
            "role": current_user.role,
            "language": current_user.language,
        }

        return render_template("chat.html", context=context)


@blp.route("/support/<string:chat_id>")
def join_conversation(chat_id):
    """Retrieve all available conversations"""
    if current_user.is_authenticated and current_user.chat_id == None:
        conversation = client.conversations.v1.conversations(chat_id).fetch()

        participants = client.conversations.v1.conversations(
            conversation.sid
        ).participants.list()

        user = None
        # check if current user is a participant of the conversation
        for participant in participants:
            if participant.identity == current_user.username:
                user = participant
                break

        if user is None:
            try:
                client.conversations.v1.conversations(
                    conversation.sid
                ).participants.create(identity=current_user.username)

            except TwilioException as err:
                print("Error:", err)

        # generate an access token
        service_sid = conversation.chat_service_sid

        token = generate_access_token(current_user.username, service_sid)

        context = {
            "token": token,
            "chat_id": conversation.sid,
            "role": current_user.role,
            "language": current_user.language,
        }

        return render_template("chat.html", context=context)
