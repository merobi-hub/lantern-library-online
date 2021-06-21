# Purpose here: ensure everyone accessing the api has a user token
# This is like @loginrequired but we're making it ourselves

from functools import wraps #wrapper
import secrets # serial ids, hextools

from flask import request, jsonify
from book_inventory.models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        #handle request
        if 'x-access-token' in request.headers:
            #set token as equal to incoming token
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        #check if incoming token matches token of current user
        try:
            current_user_token = User.query.filter_by(token = token).first()
        
        except:
            owner = User.query.filter_by(token = token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid!'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

#not using float-to-string converter here -- probably not needed (see drone inv)