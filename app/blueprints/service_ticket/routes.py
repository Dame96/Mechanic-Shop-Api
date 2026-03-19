from .schemas import service_ticket_schema, service_tickets_schema, edit_service_tickets_schema, return_service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select 
from app.models import Mechanic, Service_Ticket, db, Inventory
from . import service_ticket_bp
from app.extensions import limiter, cache
from app.utils.util import token_required


#===Create new service ticket with POST method ===#

@service_ticket_bp.route("/", methods=['POST'])
@limiter.limit("25 per day") # 25 service tickets can be created per day
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_Ticket(**service_ticket_data) #unpacks dictionary directly into our service ticket model
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201 


#==Get all service tickets===#

@service_ticket_bp.route("/", methods=['GET'])
@cache.cached(timeout=30)
def get_service_tickets():

    query = select(Service_Ticket)
    service_tickets = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(service_tickets), 200


#== Assinging a part of inventory to a service ticket ==#

@service_ticket_bp.route("/<int:service_ticket_id>/assign-inventory/<int:inventory_id>", methods=['PUT'])
def assign_inventory(service_ticket_id, inventory_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    inventory = db.session.get(Inventory, inventory_id)

    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    if not inventory:
        return jsonify({"error": "Part not found in inventory"}), 404
    
    if inventory in service_ticket.inventory:
        return jsonify({"error": "Part already assigned to this service ticket."}), 400
    
    # Appending part to relationship list "inventory", listing all the parts used for this service ticket.
    service_ticket.inventory.append(inventory)

    db.session.commit()
    return jsonify({"message": f"Part {inventory.id}, added to service ticket: {service_ticket.id}"})



#===Assign mechanic to service ticket==#

@service_ticket_bp.route("/<int:service_ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic(service_ticket_id, mechanic_id):

    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not service_ticket:
        return {"error": "Service ticket not found"}, 404
    
    if not mechanic:
        return {"error": "Mechanic not found"}, 404
    
    if mechanic in service_ticket.mechanics:
        return {"message": "Mechanic already assigned to this service ticket"}, 400
    
    # Append mechanic to relationship list (list of mechanics)
    service_ticket.mechanics.append(mechanic)

    db.session.commit()

    return {
        "message": f"Mechanic {mechanic.id} assigned to service ticket {service_ticket.id}"
    }, 200


#== Updating Mechanics on Service Ticket ==#

@service_ticket_bp.route("/<int:service_ticket_id>/edit", methods=['PUT'])
def edit_service_ticket(service_ticket_id):
    
    try:
        service_edits = edit_service_tickets_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Service_Ticket).where(Service_Ticket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    for mechanic_id in service_edits['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)



    for mechanic_id in service_edits['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)

    db.session.commit()
    return return_service_tickets_schema.jsonify(service_ticket)

#== Remove mechanic from service ticket ===#

@service_ticket_bp.route("/<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(service_ticket_id, mechanic_id):
    
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not service_ticket:
        return {"error": "Serive ticket not found "}, 404

    if not mechanic:
        return {"error": "Mechanic not found"}, 404
    
    if mechanic not in service_ticket.mechanics:
        return {"error": "Mechanic is not assigned to this service ticket"}, 400
    
    service_ticket.mechanics.remove(mechanic)

    db.session.commit()

    return {
        "message": f"Mechanic {mechanic.id} removed from service ticket {service_ticket.id}"
    }, 200



