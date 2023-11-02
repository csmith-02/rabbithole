from flask import Flask, render_template, redirect

app = Flask(__name__)

app.get('/')
def index():
    return 'Hello World'