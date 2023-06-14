from flask_pymongo import PyMongo
from flask_login import UserMixin


mongo = PyMongo()


class User(UserMixin):
    """Models a user"""

    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.language = user_data["language"]
        self.role = user_data["role"]
        self.chat_id = user_data["chat_id"]
