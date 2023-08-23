from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users
from flask_app.models import messages
from flask_app.models import passes
import re
from datetime import date, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Likes:
    DB = "match_finder1"
    def __init__(self,data):
        self.id = data['id']
        self.user_id_matcher = data['user_id_matcher']
        self.user_id_matchee = data['user_id_matchee']
        self.created_at = data['created_at']


    @classmethod
    def save_like(cls, data):
        query = "INSERT INTO likes (user_id_matcher, user_id_matchee) VALUES (%(user_id_matcher)s, %(user_id_matchee)s);"
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def get_liked_users(cls, user_id_matcher):
        query = "SELECT * FROM users JOIN likes ON users.id = likes.user_id_matchee WHERE likes.user_id_matcher = %(user_id_matcher)s;"
        data = {'user_id_matcher': user_id_matcher}
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def Unlike_User(cls, data):
        query = "DELETE FROM likes WHERE user_id_matcher = %(user_id_matcher)s AND user_id_matchee = %(user_id_matchee)s;"
        return connectToMySQL(cls.DB).query_db(query, data)



    @classmethod
    def get_users_who_liked(cls, user_id_matchee):
        query = "SELECT * FROM users JOIN likes ON users.id = likes.user_id_matcher WHERE likes.user_id_matchee = %(user_id_matchee)s;"
        data = {'user_id_matchee': user_id_matchee}
        return connectToMySQL(cls.DB).query_db(query, data)