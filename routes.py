from functools import wraps
import os
from flask import Flask, flash, redirect, render_template, request, url_for, session
from app import app
from models import Grievance, db,User
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import date, datetime

from flask_mail import Mail, Message
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

#decorator for auth_required for session check

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Please login to continue')
            return redirect(url_for('login'))
    return wrapper


@app.route('/')
def index():
    user_id = session.get('user_id')
    user = None
    if user_id:
        user = User.query.get(user_id)
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.passhash, password):
        flash('Username or password is incorrect')
        return redirect(url_for('login'))
    
    session['user_id'] = user.user_id
    return redirect(url_for('profile'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if not username or not email or not password:
        flash('Please fill all the fields')
        return redirect(url_for('register'))
    
    user= User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists')
        return redirect(url_for('register'))
    
    user= User.query.filter_by(email=email).first()
    if user:
        flash('Email already exists')
        return redirect(url_for('register'))
    
    passhash = generate_password_hash(password)

    new_user = User(username=username, email=email, passhash=passhash, is_admin=False)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/profile')
@auth_required
def profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user.is_admin:
        return render_template('adminprofile.html', user=user)
    return render_template('index.html', user=user)

@app.route('/grievance')
@auth_required
def grievance():
    user_id = session.get('user_id')
    grievances= Grievance.query.filter_by(user_id=user_id).all()
    user=None
    if user_id:
        user=User.query.get(user_id)
    return render_template('grievance.html',grievances=grievances,user=user)

@app.route('/grievance/add')
@auth_required
def add_grievance():
    user_id=session.get('user_id')
    user=User.query.get(user_id)
    return render_template('addgrievance.html',user=user)

@app.route('/grievance/add', methods=['POST'])
@auth_required
def add_grievance_post():
    user_id=session.get('user_id')
    subject=request.form['subject']
    description=request.form['description']

    if not subject or not description:
        flash('Please fill all the fields')
        return redirect(url_for('add_grievance'))

    created_on = date.today()
    grievance=Grievance(user_id=user_id,subject=subject,description=description,created_on=created_on)
    db.session.add(grievance)
    db.session.commit()
    return redirect(url_for('grievance'))

#     admin=User.query.filter_by(is_admin=True).first()
#     if admin:
#         send_email_to_admin(admin.email,grievance)
#     return redirect(url_for('grievance'))

# def send_email_to_admin(admin_email, grievance):
#     msg = Message('New Grievance Submitted',
#                   sender='mailtrap@demomailtrap.com',
#                   recipients=[admin_email])
#     msg.body = f"A new grievance has been submitted:\n\n" \
#                f"Subject: {grievance.subject}\n" \
#                f"Description: {grievance.description}\n" \
#                f"Status: {grievance.status}\n" \
#                f"Created On: {grievance.created_on}"
#     mail.send(msg)

@app.route('/grievance/<int:grievance_id>/delete')
@auth_required
def delete_grievance(grievance_id):
    grievance=Grievance.query.get(grievance_id)
    if not grievance:
        flash('Grievance not found')
        return redirect(url_for('grievance'))
    db.session.delete(grievance)
    db.session.commit()
    flash('Grievance deleted successfully')
    return redirect(url_for('grievance'))


@app.route('/allgrievances')
@auth_required
def allgrievances():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user.is_admin:
        flash('You are not authorized to view this page')
        return redirect(url_for('index'))
    grievances= Grievance.query.filter_by(status='Pending').all()
    return render_template('allgrievance.html',grievances=grievances,user=user)

@app.route('/allgrievances/<int:grievance_id>/update')
@auth_required
def update_grievance(grievance_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user.is_admin:
        flash('You are not authorized to view this page')
        return redirect(url_for('index'))
    grievance=Grievance.query.get(grievance_id)
    if not grievance:
        flash('Grievance not found')
        return redirect(url_for('allgrievances'))
    grievance.status='Resolved'
    db.session.commit()
    flash('Grievance resolved')
    return redirect(url_for('allgrievances'))