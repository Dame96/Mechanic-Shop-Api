from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, db
from . import mechanics_bp
from app.extensions import limiter, cache

#===Create new mechanic with POST method===#

@mechanics_bp.route("/", methods=['POST'])
@limiter.limit("10 per day") #only 3 mechanics can be created per day
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email']) #checking the db for a mechanic with this email

    existing_mechanic = db.session.execute(query).scalars().all()
    if existing_mechanic:
        return jsonify({"error": "Email already asscociated with an account."}), 400
    
    new_mechanic = Mechanic(**mechanic_data) #unpacks dictionary directly into our customer model
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


#===Get All Mechanics===#

@mechanics_bp.route("/", methods=['GET'])
# @cache.cached(timeout=30)
def get_mechanics():

    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Mechanic)
        mechanics = db.paginate(query, page=page, per_page=per_page)
        return mechanics_schema.jsonify(mechanics), 200
    except:
        query = select(Mechanic)
        mechanics = db.session.execute(query).scalars().all()
        return mechanics_schema.jsonify(mechanics), 200


#===Update Specific Mechanic based in UID passed in URL===#

@mechanics_bp.route("/<int:mechanic_id>", methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."})
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200



#===Deletes Specific Mechanic based on id passed through URL===#

@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
@limiter.limit("2 per day")
def delete_mechanic(mechanic_id):
    
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found"})
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic id: {mechanic_id}, successfully deleted."}), 200


# === Sort Mechanics based on popularity (amount of tickets they appear on) ==#

@mechanics_bp.route("/popular", methods=['GET'])
def popular_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    mechanics.sort(key= lambda mechanic: len(mechanic.service_tickets), reverse=True)

    return mechanics_schema.jsonify(mechanics), 200



#== New Route with Query Parameters used to search for data ==#

@mechanics_bp.route("/search", methods=['GET'])
def search_mechanic():
    name = request.args.get("name")

    query = select(Mechanic).where(Mechanic.name.like(f"%{name}%"))

    mechanics = db.session.execute(query).scalars().all()

    return mechanics_schema.jsonify(mechanics), 200


