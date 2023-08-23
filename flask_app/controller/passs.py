from flask import render_template, request, redirect,session,url_for
from flask_app.models.users import User
from flask_app.models.messages import Message
from flask_app.models.passes import Passes
from flask_app.models.likes import Likes
from flask_app.controller import message
from flask_app.controller import user
from flask_app.controller import like
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import session
import os
from flask import jsonify
import logging
from datetime import datetime



@app.route('/pass/users/<int:users_id_passed>', methods=['GET', 'POST'])
def pass_user(users_id_passed):
    if 'user_id' not in session:
        return redirect('/')

    users_id_passer = session['user_id']
    Passes.save_pass({'users_id_passer': users_id_passer, 'users_id_passed': users_id_passed})
    flash("You have passed user")
    return redirect('/home')



@app.route('/liked/passed/users')
def liked_passed_users():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    liked_users = Likes.get_liked_users(user_id)
    passed_users = Passes.get_passed_users(user_id)
    liked_by_users = Likes.get_users_who_liked(user_id)
    
    for user in liked_users:
        birth_date = user['birthday']
        age = (datetime.today().date() - birth_date).days // 365
        user['age'] = age


    for user in passed_users:
        birth_date = user['birthday']
        age = (datetime.today().date() - birth_date).days // 365
        user['age'] = age
    return render_template('liked_and_passed_users.html', liked_users=liked_users, passed_users=passed_users, liked_by_users=liked_by_users)


@app.route('/unpass/user/<int:user_id_passed>', methods=['POST'])
def unpass_user(user_id_passed):
    if 'user_id' not in session:
        return redirect('/')
    users_id_passer = session['user_id']
    Passes.unpass_user({'users_id_passer': users_id_passer, 'users_id_passed': user_id_passed})
    return redirect('/liked/passed/users')