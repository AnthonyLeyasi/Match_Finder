from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users
from flask_app.models import messages
from flask_app.models import likes
import re
from datetime import date, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Passes:
    DB = "match_finder1"
    def __init__(self,data):
        self.id = data['id']
        self.users_id_passer = data['users_id_passer'] #matcher
        self.users_id_passed = data['users_id_passed']#matchee
        self.created_at = data['created_at']


    @classmethod
    def save_pass(cls, data):
        query = "INSERT INTO passes (users_id_passer, users_id_passed) VALUES (%(users_id_passer)s, %(users_id_passed)s);"
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def get_passed_users(cls, users_id_passer):
        query = "SELECT * FROM users JOIN passes ON users.id = users_id_passed WHERE users_id_passer = %(users_id_passer)s;"
        data = {'users_id_passer': users_id_passer}
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def unpass_user(cls, data):
        query = "DELETE FROM passes WHERE users_id_passer = %(users_id_passer)s AND users_id_passed = %(users_id_passed)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
