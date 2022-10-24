import functools

from flask import Blueprint, jsonify, request
from lightMed.models.models import User, UserSchema
from flask_jwt_extended import create_access_token


bp = Blueprint('auth_jwt', __name__, url_prefix='/auth_jwt')

@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.is_json:
        user = request.json["user_name"]
        password = request.json["user_password"]
    else:
        user = request.args.get("user_name")
        password = request.args.get("user_password")

    test = User.query.filter_by(user_name=user, user_password=password).first()
    if test:
        access_token = create_access_token(identity=test.user_id)
        return jsonify(message="You are logged in", access_token=access_token), 201
    else:
        return jsonify(message="You are not authorized to log in"), 401

