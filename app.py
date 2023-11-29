from flask import Flask, abort, render_template, redirect, request, send_from_directory, session
from datetime import datetime
import os
from dotenv import load_dotenv
from models import User, Post, Community, db
from flask_bcrypt import Bcrypt
import re

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

load_dotenv()

app = Flask(__name__, static_url_path='/rabbithole/static')

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

app.secret_key = os.getenv('APP_SECRET_KEY', 'strawberry')
db.init_app(app)
bcrypt = Bcrypt(app)

app.config['UPLOAD_FOLDER'] = '/rabbithole/static/user_profile_images'

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
        user = User.query.filter_by(username=session['username']).first()
    else:
        loggedIn=False
        user = None
    communities = Community.query.all()

    return render_template('community_page.html', loggedIn=loggedIn, communities=communities, user=user)

@app.get('/profile')
def profile():
    if 'username' not in session:
        return redirect('/login', 302)

    user = User.query.filter_by(username=session['username']).first()
    return render_template('profile_page.html', user=user, loggedIn=True)


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

@app.route('/contact_us')
def contact():
    if 'username' in session:
        loggedIn=True
        user = User.query.filter_by(username=session['username']).first()
    else:
        loggedIn=False
        user = None
    return render_template('contact_us_page.html')

@app.route('/about_us')
def about():
    if 'username' in session:
        loggedIn=True
        user = User.query.filter_by(username=session['username']).first()
    else:
        loggedIn=False
        user = None
    return render_template('about_us_page.html')

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

@app.route('/profile/edit_username', methods=['POST'])
def edit_username():
    if 'username' not in session:
        return redirect('/login', 302)
    new_username = request.form.get('username')
    user = User.query.filter_by(username=session['username']).first()
    # Check if the new username is already taken
    if User.query.filter_by(username=new_username).first():
        return render_template('profile_page.html', error="Username already taken")
    user.username = new_username
    db.session.commit()
    session['username'] = new_username
    return redirect('/profile')


# Communities Functionality

@app.get('/communities/create')
def get_create_page():
    return render_template('create_community.html', loggedIn=True)

@app.post('/communities/create')
def create_community():
    # check if user is logged in, else prompt to login first
    if 'username' not in session:
        return redirect('/login', error="You must login before creating a community.")
    # Get form data for creating a community
    name = request.form.get('name')
    subject_id = request.form.get('subject')
    if int(subject_id) == 1:
        subject = 'Business'
    elif int(subject_id) == 2:
        subject = 'School'
    elif int(subject_id) == 3:
        subject = 'Politics'
    elif int(subject_id) == 4:
        subject = 'Sports'
    elif int(subject_id) == 5:
        subject = 'Relationships'
    elif int(subject_id) == 6:
        subject = 'Miscellaneous'
    else:
        abort(400)
    if not name or not subject:
        abort(400)
    # Check if name is already taken
    community = Community.query.filter_by(name=name).first()
    if not community:
        redirect('/communities/create', 302)
    # Create community with data and current user as owner
    user = User.query.filter_by(username=session['username']).first()
    community = Community(name=name, subject=subject, pfpic='default.png', owner_id=user.id)
    # append community to user_community
    db.session.add(community)
    user.communities.append(community)
    db.session.commit()

    return redirect('/communities', 302)

@app.post('/communities/join/<id>')
def join_community(id: int):
    if 'username' not in session:
        redirect('/login', 302)
    # Add user to the community
    user = User.query.filter_by(username=session['username']).first()
    community = Community.query.filter_by(id=id).first()
    user.communities.append(community)
    db.session.commit()
    return redirect('/communities', 302)

@app.post('/communities/delete/<id>')
def delete_community(id):
    if 'username' not in session:
        redirect('/login', 302)
    user = User.query.filter_by(username=session['username']).first()
    community = Community.query.filter_by(id=id).first()
    if user.id != community.owner_id:
        abort(400)

    db.session.delete(community)
    db.session.commit()
    return redirect('/communities', 302)
    
@app.post('/communities/remove/<id>')
def remove_community(id):
    if 'username' not in session:
        redirect('/login', 302)
    user = User.query.filter_by(username=session['username']).first()
    community = Community.query.filter_by(id=id).first()
    if user.id == community.owner_id:
        abort(400)
    
    user.communities.remove(community)
    db.session.commit()
    return redirect('/communities', 302)
# Post Functionality

@app.get('/post/create')
def get_create_post():
    if 'username' not in session:
        return redirect('/login', 302)
    return render_template('create_post.html', loggedIn=True)