from flask import render_template, request, redirect,session,url_for,jsonify
from flask_app.models.users import User
from flask_app.models.messages import Message
from flask_app.models.likes import Likes
from flask_app.models.passes import Passes
from flask_app.controller import message
from flask_app.controller import like
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import session
from datetime import datetime
import os
from flask import jsonify
import googlemaps
from dotenv import load_dotenv




UPLOAD_FOLDER = 'flask_app/static/uploaded_images'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


load_dotenv()

#Nav Bar Greeting Page
@app.route('/')
def index():
    return redirect('/greet')


@app.route('/greet')
def create():
    return render_template('greet.html')

@app.route('/carrer')
def carrer():
    return render_template('careers.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/info')
def info():
    return render_template('info.html')



#register
@app.route('/register')
def display_form():
    return render_template('register.html')

@app.route('/register/user', methods=['POST'])
def register():
    if 'profile_pic' not in request.files:
        flash("Profile picture is required.")
        return redirect('/register')

    profile_pic = request.files['profile_pic']

    is_valid = User.validate_user(request.form)

    if is_valid:
        if request.form['password'] == '':
            flash("Password is required.")
            return redirect('/register')

        # Check if the email is already registered
        existing_user = User.get_user_by_email({'email': request.form['email']})
        if existing_user:
            flash("Email already exists. Please choose a different email.")
            return redirect('/register')

    if 'profile_pic' not in request.files:
        flash("Profile picture is required.")
        return redirect('/register')

    profile_pic = request.files['profile_pic']
    if profile_pic.filename.split('.')[-1].lower() not in ALLOWED_EXTENSIONS:
        flash("File type not allowed.")
        return redirect('/register')

    filename = os.path.join(UPLOAD_FOLDER, profile_pic.filename)
    profile_pic.save(filename)

    is_valid = User.validate_user(request.form)

    if is_valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "location": request.form['location'],
            "email": request.form['email'],
            "password": pw_hash,
            "birthday": request.form['birthday'],
            "gender": request.form['gender'],
            "profile_pic": 'uploaded_images/' + profile_pic.filename
        }
        
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect('/home')
    else:
        return redirect('/register')







#Login
@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/login/user',methods=['POST'])
def user_login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/home')


#Home page



@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session.get('user_id')
    
    liked_users = [user['user_id_matchee'] for user in Likes.get_liked_users(user_id)]
    passed_users = [user['users_id_passed'] for user in Passes.get_passed_users(user_id)]

    excluded_users = set(liked_users + passed_users + [user_id])  
    users = User.get_all_except(excluded_users) 

    user = users[0] if users else None

    if user:
        birth_date = user['birthday']
        age = (datetime.today().date() - birth_date).days // 365
        user['age'] = age

    return render_template('home.html', user=user)



#Users CRUD
@app.route('/view/user/info/')
def view_user_info():
    if 'user_id' not in session:
        return redirect('/login')
    id = session.get('user_id') 
    user = User.get_by_id({'id': id})
    return render_template('show.html', user=user)



@app.route('/destroy/users/<int:id>')
def delete_user(id):
    if 'user_id' not in session:
        return redirect('/login')
    User.destroy({'id': id})
    return redirect('/')


@app.route('/edit/user/info', methods=['GET', 'POST'])
def edit_user_info():
    if 'user_id' not in session:
        return redirect('/login')
    id = session.get('user_id')
    if request.method == 'POST':
        data = {
            "id": id,
            "first_name": request.form.get('first_name'),
            "last_name": request.form.get('last_name'),
            "location": request.form.get('location'),
            "email": request.form.get('email'),
            "profile_pic": request.files.get('profile_pic')
        }

        is_valid = User.edit_user(data)

        if is_valid:
            user = User.update(data)
            flash("User information updated successfully.")
            return redirect('/view/user/info/')
        else:
            return redirect('/edit/user/info')
    else:
        user = User.get_by_id({'id': id})
        return render_template('Edit_User.html', user=user)

@app.route('/find/a/match', methods=['Get','POST'])
def find_a_match():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('find_a_match.html')


