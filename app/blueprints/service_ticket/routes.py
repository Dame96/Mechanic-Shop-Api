from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select 
from app.models import Mechanic, Service_Ticket, db
from . import service_ticket_bp


#===Create new service ticket with POST method ===#

@service_ticket_bp.route("/", methods=['POST'])
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
def get_service_tickets():

    query = select(Service_Ticket)
    service_tickets = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(service_tickets), 200


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
    
    # Append mechanic to relationship list
    service_ticket.mechanics.append(mechanic)

    db.session.commit()

    return {
        "message": f"Mechanic {mechanic.id} assigned to service ticket {service_ticket.id}"
    }, 200


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



