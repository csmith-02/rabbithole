from flask import Flask, abort, render_template, redirect, request, send_from_directory, session
from datetime import datetime
import os
from dotenv import load_dotenv
from models import User, Post, Community, db
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__, static_url_path='/rabbithole/static')

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

app.secret_key = os.getenv('APP_SECRET_KEY', 'strawberry')
db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/rabbithole/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.get('/')
def index():
    if 'username' in session:
        return redirect('/home')
    return render_template('landing_page.html')

@app.route('/home')
def home():
    if 'username' not in session:
        # Redirect the user to login to access the home route
        return redirect('/login', 302)
    return render_template('home_page.html', username=session['username'], loggedIn=True)

@app.route('/communities')
def community():
    if 'username' in session:
        loggedIn=True
        communities = User.query.filter_by(username=session['username']).all()
    else:
        communities = Community.query.all()
        loggedIn=False
    
    return render_template('community_page.html', loggedIn=loggedIn, communities=communities)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        raw_password = request.form.get('password')
        
        if perform_login(username, raw_password):
            return redirect('/home')
        else:
            return render_template('login_page.html', error="Invalid username or password")
    if 'username' in session:
        return redirect('/home', 302)
    return render_template('login_page.html', loggedIn=False)

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        raw_password = request.form.get('password')
        
        if perform_signup(username, email, raw_password):
            print("User was created!")
        else:
            return render_template('signup_page.html', error="Username already taken")
    if 'username' in session:
        return redirect('/home', 302)
    return render_template('signup_page.html', loggedIn=False)

@app.post('/logout')
def logout():
    del session['username']
    return redirect('/')

def perform_login(username, raw_password):
    if not username or not raw_password:
        abort(401)
    
    existing_user = User.query.filter_by(username=username).first()
    
    if not existing_user or not bcrypt.check_password_hash(existing_user.hashpw, raw_password):
        return False
    
    session['username'] = username
    return True

def perform_signup(username, email, raw_password):
    if not username or not raw_password:
        abort(400)
    
    existing_user = User.query.filter_by(username=username).first()
    
    if existing_user:
        return False  
    
    hashpw = bcrypt.generate_password_hash(raw_password, 12).decode()
    new_user = User(username=username, email=email, hashpw=hashpw)
    db.session.add(new_user)
    db.session.commit()
    
    return True 
