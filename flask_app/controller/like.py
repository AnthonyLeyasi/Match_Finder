from flask import render_template, request, redirect,session,url_for
from flask_app.models.users import User
from flask_app.models.messages import Message
from flask_app.models.likes import Likes
from flask_app.models.passes import Passes
from flask_app.controller import message
from flask_app.controller import user
from flask_app.controller import passs
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import session
import os
from datetime import datetime
from flask import jsonify
import logging



@app.route('/like/users/<int:user_id_matchee>', methods=['POST'])
def like_user(user_id_matchee):
    if 'user_id' not in session:
        return redirect('/')

    user_id_matcher = session['user_id']


    data = {'user_id_matcher': user_id_matcher, 'user_id_matchee': user_id_matchee}
    existing_likes = Likes.get_users_who_liked(user_id_matchee)
    existing_like = existing_likes[0] if existing_likes else None

    if not existing_like:
        Likes.save_like({'user_id_matcher': user_id_matcher, 'user_id_matchee': user_id_matchee})
        flash("You have liked this user.")
    else:
        flash("You have already liked this user.")

    return redirect('/home')




@app.route('/unlike/liked/user/<int:user_id_matchee>', methods=['POST'])
def Unlike_Liked_user(user_id_matchee):
    if 'user_id' not in session:
        return redirect('/')
    user_id_matcher = session['user_id']
    Likes.Unlike_User({'user_id_matcher': user_id_matcher, 'user_id_matchee': user_id_matchee})
    return redirect('/liked/passed/users')




@app.route('/view/user/<int:user_id>')
def view_user(user_id):
    if 'user_id' not in session:
        return redirect('/')
    user_profile = User.get_user_by_id(user_id) 

    birth_date = user_profile.birthday
    age = (datetime.today().date() - birth_date).days // 365
    user_profile.age = age   
    return render_template('view_liked_passed_user.html', user=user_profile)