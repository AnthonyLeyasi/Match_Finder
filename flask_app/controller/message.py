from flask import render_template, request, redirect,session
from flask_app.models.users import User
from flask_app.models.messages import Message
from flask_app.controller import user
from flask_app.controller import message
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import session
import os
UPLOAD_FOLDER = 'flask_app/static/uploaded_images'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}



@app.route('/message/users')
def message():
    if ('user_id') not in session:
        redirect('/')
    loged_in_user = session['user_id']
    users = User.get_all_except_users_in_messages(loged_in_user)
    return render_template('messages.html', users=users)




@app.route('/message/users/text/<int:recipient_id>', methods=['GET', 'POST'])
def text_users(recipient_id):
    if ('user_id') not in session:
        redirect('/')
    messages = Message.get_users_messages(recipient_id)
    user_id_recipient = recipient_id
    return render_template('text_user.html', messages=messages, user_id_recipient=user_id_recipient)



@app.route('/message/users/text/send', methods=['POST'])
def send_message():
    if ('user_id') not in session:
        redirect('/')

    data = {
        "text": request.form['text'],
        "user_id_sender": request.form['user_id_sender'],
        "user_id_recipient": request.form['user_id_recipient']
    }
    message = Message.save_message(data)
    if message:
        flash("Message Sent!!!")
        recipient_id = int(request.form['user_id_recipient'])
        return redirect(f'/message/users/text/{recipient_id}')
    else:
        flash("Failed to send message.")
        return redirect('/message/users')