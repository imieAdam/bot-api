from flask import current_app
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def init_jwt():
    jwt.init_app(current_app)