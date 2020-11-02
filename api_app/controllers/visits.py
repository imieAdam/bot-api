import functools

from flask import Blueprint, jsonify, request
from api_app.models.models import (Visit, VisitToLocation, User, Specialization, TimeFrame, Location,
                                    VisitSchema, VisitToLocationSchema, UserSchema,  SpecializationSchema, TimeFrameSchema, LocationSchema)
from flask_jwt_extended import jwt_required, get_jwt_identity
from api_app.database.database import db_session

bp = Blueprint('visits', __name__)


@bp.route('/visits', methods=['GET'])
#@jwt_required
#TODO -> filter visits by user_id
def get_visits():    
    visit_schema = VisitSchema(many=True)
    visit = Visit.query.all()
    result = visit_schema.dump(visit)
    return jsonify(visit=result)


@bp.route('/visit', methods=['GET'])
#@jwt_required
def get_visit():    
    visit_schema = VisitSchema()
    if request.is_json:
        visit_id = request.json["visit_id"]
    else:
        visit_id = request.args.get("visit_id")

    visit = Visit.query.filter(Visit.visit_id == visit_id).first()
    #visit_list = Visit.query.all()
    result = visit_schema.dump(visit)
    return jsonify(visit=result)


@bp.route('/visit', methods=['POST'])
@jwt_required
def post_visit():
    if request.is_json:        
        visits_schema = VisitSchema()
        visit_to_locations_schema = VisitToLocationSchema(many=True)
        time_frames_schema = TimeFrameSchema(many=True)
        user = get_jwt_identity()
        specialization = request.json["specialization_id"]
        after_date = request.json["after_date"]
        visit_to_locations = visit_to_locations_schema.load(request.json["locations"])
        time_frames = time_frames_schema.load(request.json["time_frames"])

        visit = Visit(specialization_id=specialization, 
                after_date=after_date,
                locations=visit_to_locations,
                time_frames=time_frames,
                user_id=int(user)
                )
        db_session.add(visit)
        db_session.commit()
        return jsonify(message="Visit created", visit=visits_schema.dump(visit))
    else:
        return jsonify(message="Please use JSON")


@bp.route('/visit', methods=["DELETE"])
#@jwt_required
def delete_visit():
    if request.is_json:
        visit_id = request.json["visit_id"]
    else:
        visit_id = request.args.get("visit_id")

    visit = Visit.query.filter(Visit.visit_id == visit_id).first()
    if visit:
        db_session.delete(visit)
        db_session.commit()
        return jsonify(message="Visit deleted")
    else:
        return jsonify(message="Invalid id")
    

@bp.route('/visit', methods=["PUT"])
#@jwt_required
def update_visit():
    if request.is_json:
        visit_id = request.json["visit_id"]
        booked_date_time = request.json["booked_date_time"]
        booked_location = request.json["booked_location"]
    else:
        visit_id = request.args.get("visit_id")
        booked_date_time = request.args.get("booked_date_time")
        booked_location = request.args.get("booked_location")
    
    visit = Visit.query.filter(Visit.visit_id == visit_id).first()
    if visit:
        if booked_date_time:
            visit.booked_date_time = booked_date_time
            visit.booked_location = booked_location
        else:
            visit.booked_date_time = None
            visit.booked_location = None
        db_session.commit()
        return jsonify(message="Visit updated")
    else:
        return jsonify(message="There is no visit with such ID")
