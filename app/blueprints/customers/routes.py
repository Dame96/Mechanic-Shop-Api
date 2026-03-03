from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db, Service_Ticket
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required
from app.blueprints.service_ticket.schemas import service_tickets_schema



#== Login Route that grants users a token ==# 

@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials["email"]
        password = credentials["password"]
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password'}), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalar_one_or_none() #Query customer table for a customer with this email

    if customer and customer.password == password: # if we have a customer associated with the email, validate the password
        
        auth_token = encode_token(customer.id)

        response = {
            "status": "success", 
            "message": "Successfully Logged in", 
            "auth_token": auth_token
        } # token encoded and returned to the user/client

        return jsonify(response), 200
    else:
        return jsonify({'messages': "Invalid email or password"}), 401


#===Create Customer (POST) this endpoint create a new customer by deserializing and validating the incoming data

@customers_bp.route("/", methods=['POST'])
@limiter.limit("5 per day") # A client can only attempt to make 5 users per hour.
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email']) #checking our db for a customer with this email 

    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
         return jsonify({"error": "Email already associated with an account."}), 400
    
    new_customer = Customer(**customer_data) #unpacks json data that was sent with request directly into our customer model creating a new instance
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201




#=====GET All Customers
# when this request is received a function to retrieve and return all Customers will fire. 

@customers_bp.route("/", methods=['GET'])
# @cache.cached(timeout=60)
def get_customers():
    
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    
    except:
        query = select(Customer)
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers), 200


#===GET SPECIFIC CUSTOMER, using customer id

@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
          return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404


#== Get service tickets for logged in customer ==#
@customers_bp.route("/my-tickets", methods=['GET'])
@token_required
def get_customers_tickets(customer_id):

    query = select(Service_Ticket).where(Service_Ticket.customer_id == customer_id)

    service_tickets = db.session.execute(query).scalars().all()
        
    return service_tickets_schema.dump(service_tickets), 200

#===Update Specific Customer Using ID and PUT method.

@customers_bp.route("/", methods=['PUT']) 
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

     
#===Delete Specific Customer Using Id===#
@customers_bp.route("/", methods=['DELETE'])
@limiter.limit("10 per day") # only 10 customers can be deleted per day
@token_required
def delete_customer(customer_id): #Receiving the customer_id from the token
    
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()


    if not customer:
        return jsonify({"error": "Customer not found."})
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer id: {customer_id}, successfully deleted."}), 200
    