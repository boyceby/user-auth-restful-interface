'''
Authorization Blueprint
'''

import json
import argon2
import functools
from flask import Blueprint, request, make_response, session
from backend.user_ORM import User, UserDataException

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/registrations', methods=['POST'])
def registerUser():
    try:
        user = User.createFromJSON(request.json)
    except UserDataException as e:
        return make_response(str(e), 400)
    session['username'] = user.getUsername()
    return  {
                'status': "created",
                'user': user.jsonable()
            }

@bp.route('/sessions', methods=['POST', 'DELETE'])
def logInOut():
    if request.method == 'POST':
        json_data = request.json
        valid_user = User.verifyValidUser(json_data['username'], json_data['password'])
        if not valid_user:
            return make_response("Invalid login credentials.", 400)
        else:
            user = User.findByUsername(json_data['username'])
            session['username'] = user.getUsername()
            return  {
                        'logged_in': True,
                        'user': user.jsonable()
                    }
    session.pop('username', default=None)
    return {'logged_in': False}

@bp.route('/logged_in', methods=['GET'])
def loggedIn():    
    if 'username' not in session:
        return {'logged_in': False}
    else:
        return  {
                    'logged_in': True,
                    'user': User.findByUsername(session['username']).jsonable()
                }
