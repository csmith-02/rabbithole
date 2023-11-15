from flask import Flask, render_template, redirect, send_from_directory
from datetime import datetime
from flask import Flask, render_template, redirect
import os
from dotenv import load_dotenv
from models import User, Post, Community, db

load_dotenv()

app = Flask(__name__, static_url_path='/rabbithole/static')

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

db.init_app(app)

@app.route('/rabbithole/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.get('/')
def index():
    return render_template('landing_page.html')

@app.route('/home_page.html')
def home():
    return render_template('home_page.html')

@app.route('/community_page.html')
def community():
    return render_template('community_page.html')

@app.route('/login_page.html')
def login():
    return render_template('login_page.html')

@app.route('/signup_page.html')
def signup():
    return render_template('signup_page.html')
