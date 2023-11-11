from datetime import datetime
from flask import Flask, render_template, redirect
import os
from dotenv import load_dotenv
from models import User, Post, Community, db

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

db.init_app(app)

@app.get('/')
def index():
    return 'Hello World'