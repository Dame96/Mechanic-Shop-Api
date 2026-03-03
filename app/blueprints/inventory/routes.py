from .schemas import inventory_schema, inventorys_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Inventory, db
from . import inventory_bp
from app.extensions import limiter, cache


#== Create a new "part" record in the inventory table ==#

@inventory_bp.route("/", methods=['POST'])
def create_inventory():

    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_inventory = Inventory(**inventory_data) # unpacks json data directly into our Inventory model, instanciating a new model
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201


#== GET all parts from inventory table ==#

@inventory_bp.route("/", methods=['GET'])
def get_inventory():

    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Inventory)
        parts = db.paginate(query, page=page, per_page=per_page)
        return inventorys_schema.jsonify(parts), 200
    except:
        query = select(Inventory)
        parts = db.session.execute(query).scalars().all()
        return inventorys_schema.jsonify(parts), 200
    

#== Update specific product based on ID passed in ==# 

@inventory_bp.route("/<int:inventory_id>", methods=['PUT'])
def update_inventory(inventory_id):

    inventory = db.session.get(Inventory, inventory_id)
    
    if not inventory:
        return jsonify({"error": "Part not found."}), 404

    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in inventory_data.items():
        setattr(inventory, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200
        






#== Delete a part from the inventory table using id in route ==#


@inventory_bp.route("<int:inventory_id>", methods=['DELETE'])
def delete_inventory(inventory_id):

    query = select(Inventory).where(Inventory.id == inventory_id)
    part = db.session.execute(query).scalars().first()

    if not part:
        return jsonify({"error": "Part not found in inventory records."})
    
    db.session.delete(part)
    db.session.commit()
    
    return jsonify({"message": f"Part ID: {inventory_id}, successfully deleted from inventory records."}), 200
