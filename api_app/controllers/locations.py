import functools

from flask import Blueprint, jsonify, request
from api_app.models.models import (Location, LocationSchema, City, CitySchema)
from flask_jwt_extended import jwt_required
from api_app.database.database import db_session


bp = Blueprint('locations', __name__)

@bp.route('/cities', methods=["GET"])
def get_cities():
    city_schema = CitySchema(many=True)
    city_list = City.query.all()
    result = city_schema.dump(city_list)
    return jsonify(cities=result), 200

@bp.route('/city_locations', methods=["GET"])
def get_city_locations():

    if request.is_json:
        city_id = request.json["city_id"]
    else:
        city_id = request.args["city_id"]

    location_schema = LocationSchema(many=True)
    location_list = Location.query.filter(Location.city_id == city_id).all()
    result = location_schema.dump(location_list)
    return jsonify(locations=result)

@bp.route('/locations', methods=['GET'])
#@jwt_required
def locations():    
    location_schema = LocationSchema(many=True)
    location_list = Location.query.all()
    result = location_schema.dump(location_list)

    return jsonify(results=result)

@bp.route('/location', methods=['GET'])
#@jwt_required
def get_location():
    if request.is_json:
        location_id = request.json["location_id"]
    else:
        location_id = request.args.get("location_id")

    location_schema = LocationSchema()
    location = Location.query.filter(Location.location_id == location_id).first()
    if location:
        result = location_schema.dump(location)
        return jsonify(results=result)
    else:
        return jsonify(message="Invalid id"), 404

@bp.route("/location", methods=["POST"])
#@jwt_required
def put_location():
    if request.is_json:
        address = request.json["address"]
        city_name = request.json["city_id"]
    else:
        address = request.args.get("address")
        city_id = request.args.get("city_id")
    
    location = Location(address=address, city_id=city_id)
    exists = Location.query.filter(Location.city_id == location.city_id and Location.address == location.address).first()
    if not exists:
        db_session.add(location)
        db_session.commit()
        return jsonify(message="Location added"), 201
    else:
        return jsonify(message="Location already exists"), 409

    

@bp.route("/location", methods=["DELETE"])
#@jwt_required
def delete_location():
    if request.is_json:
        location_id = request.json["location_id"]
    else:
        location_id = request.args.get("location_id")
    
    location = Location.query.filter(Location.location_id==location_id).first()

    if location:
        db_session.delete(location)
        db_session.commit()
        return jsonify(message="Location deleted"), 202
    else:
        return jsonify(message="Invalid id"), 404

'''
@bp.route('/visit_to_locations', methods=['GET'])
def visit_to_locations():    
    visit_to_locations_schema = VisitToLocationSchema(many=True)
    visit_to_locations_list = VisitToLocation.query.all()
    result = visit_to_locations_schema.dump(visit_to_locations_list)
    return jsonify(results=result)


@bp.route('/users', methods=['GET'])
def users():    
    user_schema = UserSchema(many=True)
    user_list = User.query.all()
    result = user_schema.dump(user_list)
    return jsonify(results=result)
'''