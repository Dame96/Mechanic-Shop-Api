from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify
import os 

SECRET_KEY = os.environ.get('SECRET_KEY') or "super secret secrets" #secret keys are used to sign tokens, encode and decode the tokens


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Look for token in the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing! Please confirm that you are logged in!'}), 401
        
        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = data['sub'] #Fetch the user ID

        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(user_id, *args, **kwargs)
    
    return decorated



def encode_token(user_id): #using unique pieces of info to make tokens user specific
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), # Setting the expiration time of the token to an hour past now
        'iat': datetime.now(timezone.utc), # Issued at time - time token was issued/created.
        'sub': str(user_id) # 'sub' stands for subject. This needs to be a string or the token will be malformed and wont be able to be decoded.
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') #hashing algorithm, used for scrambling. 

    return token

