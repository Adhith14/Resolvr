from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db=SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passhash = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

class Grievance(db.Model):
    grievance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(80), nullable=False, default='Pending')
    created_on = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User', backref=db.backref('grievances', lazy=True))

with app.app_context():
    db.create_all()

    # admin=User.query.filter_by(is_admin=True).first()
    # if not admin:
    #     passwordhash = generate_password_hash('admin')
    #     admin=User(username='admin',email='adhithkl2003@gmail.com',passhash=passwordhash,is_admin=True)
    #     db.session.add(admin)
    #     db.session.commit()
