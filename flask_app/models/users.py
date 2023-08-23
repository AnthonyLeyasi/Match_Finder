from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import likes
from flask_app.models import messages
from flask_app.models import passes
import re
from datetime import date, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "match_finder1"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.location = data['location']
        # self.latitude = data['latitude']  
        # self.longitude = data['longitude']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.gender = data['gender']
        self.profile_pic = data['profile_pic']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_user(user_data):
        required_keys = ['first_name', 'last_name', 'location', 'email', 'password', 'confirm_password', 'birthday']
        empty_fields = []

        for key in required_keys:
            if not user_data[key].strip():
                empty_fields.append(key)

        if empty_fields:
            for field in empty_fields:
                flash(f"{field.replace('_', ' ').title()} is required.")
            return False


        if len(user_data['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            return False

        if len(user_data['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            return False

        if len(user_data['location']) < 2:
            flash("Location is required.")
            return False

        if not re.match(EMAIL_REGEX, user_data['email']):
            flash("Invalid email address.")
            return False

        if len(user_data['password']) < 6:
            flash("Password must be at least 6 characters.")
            return False

        if user_data['password'] != user_data['confirm_password']:
            flash("Passwords do not match.")
            return False

        if not re.search(r'[A-Z]', user_data['password']):  # Check for at least one uppercase letter
            flash("Password must contain at least one uppercase letter.")
            return False

        if not re.search(r'\d', user_data['password']):  # Check for at least one digit
            flash("Password must contain at least one digit.")
            return False

        try:
            birthday = datetime.strptime(user_data['birthday'], '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid birthday format. Please use YYYY-MM-DD.")
            return False

        current_date = date.today()
        age = current_date.year - birthday.year - ((current_date.month, current_date.day) < (birthday.month, birthday.day))

        if age < 18:
            flash("You must be 18 or older to join.")
            return False

        return True


#edit User info 
    @staticmethod
    def edit_user(user_data):
        required_keys = ['first_name', 'last_name', 'location', 'email']
        empty_fields = []

        for key in required_keys:
            if not user_data[key].strip():
                empty_fields.append(key)

        if empty_fields:
            for field in empty_fields:
                flash(f"{field.replace('_', ' ').title()} is required.")
            return False


        if len(user_data['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            return False

        if len(user_data['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            return False

        if len(user_data['location']) < 2:
            flash("Location is required.")
            return False

        if not re.match(EMAIL_REGEX, user_data['email']):
            flash("Invalid email address.")
            return False

        return True





# Save
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,location,email,password,birthday,gender,profile_pic ) VALUES ( %(first_name)s , %(last_name)s,%(location)s,%(email)s,%(password)s,%(birthday)s,%(gender)s,%(profile_pic)s );"
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, location = %(location)s, email = %(email)s,profile_pic = %(profile_pic)s WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_except_users_in_messages(cls, user_id):
        query = "SELECT * FROM users WHERE id != %(user_id)s"
        data = {
        'user_id': user_id
    }
        results = connectToMySQL(cls.DB).query_db(query, data)
        users = []
        for result in results:
            users.append(cls(result))
        return users

    @classmethod
    def get_all_except(cls, excluded_users):
        excluded_users_str = ','.join(map(str, excluded_users))
        query = f"SELECT * FROM users WHERE id NOT IN ({excluded_users_str})"
        return connectToMySQL(cls.DB).query_db(query)


    @classmethod
    def get_user_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        data = {'user_id': user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None

    @classmethod
    def get_next_unliked_user(cls, current_user_id):
        query = """SELECT * FROM users 
            WHERE id != %(user_id)s 
            AND id NOT IN (SELECT user_id_matchee FROM likes WHERE user_id_matcher = %(user_id)s)
            LIMIT 1;"""
        data = {'user_id': current_user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None