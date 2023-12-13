from app import app, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest

@pytest.fixture
def set():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(set):
    return set.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home_page_unauthenticated_user(client):
    response = client.get('/home')
    assert response.status_code == 302  # Expecting a redirect

def test_profile_page_unauthenticated_user(client):
    response = client.get('/profile')
    assert response.status_code == 302  # Expecting a redirect
    assert response.headers['Location'] == '/login'

def test_create_community_page_unauthenticated_user(client):
    response = client.get('/communities/create')
    assert response.status_code == 200

def test_friends_page_unauthenticated_user(client):
    response = client.get('/communities/friends')
    assert response.status_code == 200