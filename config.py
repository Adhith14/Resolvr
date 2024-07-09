from dotenv import load_dotenv
import os

from app import app

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')


app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = '73e081c3a979632cba1efa26d48c8486'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False