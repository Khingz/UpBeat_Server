#!/usr/bin/env python3
"""User routes"""
from flask import Blueprint, jsonify, request
from models.user import User
from models import storage
from flask_login import login_user, current_user, login_required, logout_user
import re

user = Blueprint('user', __name__)


def validate_email(email):
    # Basic email regex pattern
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

@user.route('/login', methods=['GET', 'POST'], endpoint='login', strict_slashes=False)
def login():
    """Login route"""
    from api.v1 import bcrypt
    if current_user.is_authenticated:
        return jsonify({'messasge': 'already logged in'})
    email  = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return jsonify({'error': 'email and password is required'})
    user = storage.get_email(User, email.lower())
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=True)
        return jsonify({'message': 'user logged in successfully'}), 200
    return jsonify({'error': 'invalid email or password'}), 400


@user.route('/register', methods=['GET', 'POST'], endpoint='register', strict_slashes=False)
def register():
    """Register route"""
    from api.v1 import bcrypt

    if current_user.is_authenticated:
        return jsonify({'messasge': 'already logged in'})
    
    new_user_data = {
        'username': request.form.get('username'),
        'email': request.form.get('email'),
        'password': bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8'),
        'first_name': request.form.get('firstname'),
        'last_name': request.form.get('lastname')
    }
    # Validate form data
    if not new_user_data['username'] or not new_user_data['email'] or not new_user_data['password'] or not new_user_data['first_name'] or not new_user_data['last_name']:
        return jsonify({'error': 'all fields are required'}), 400
    
    # Email validation
    if not validate_email(new_user_data['email']):
        return jsonify({'error': 'invalid email address'}), 400
    
    #check if user already exist
    existing_email = storage.get_email(User, new_user_data['email'])
    if existing_email:
        return jsonify({'error': 'user already exist'}), 400
    
    # Create new User
    new_user = User(**new_user_data)
    # Save User in database
    new_user.save()
    return jsonify({'message': 'user created successfully'})

@user.route("/logout", strict_slashes=False)
@login_required
def logout():
    """Log out a user"""
    logout_user()
    return jsonify({'message': 'user logged out successfully'})

@user.route('/<user_id>', methods=['GET'], strict_slashes=False)
def single_user(user_id):
    """ Get single user
    """
    user = storage.get(User, user_id)
    if user:
        playlists = []
        for item in user.playlists:
            playlists.append(item.to_dict())
        user = user.to_dict()
        user['playlists'] = playlists
        return jsonify(user), 200
    else:
        return jsonify({'message': 'playlist not found'}), 404
