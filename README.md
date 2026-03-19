MECHANIC SHOP-API

A RESTful API built with Flask, SQLAlchemy, Marshmallow, and the Application Factory Pattern to manage a mechanic shop system.

This API allows you to manage:

CUSTOMERS:

MECHANICS: 

SERVICE TICKETS:

Mechanic ↔ Service Ticket assignments (Many-to-Many relationship)

Inventory ↔ Service Ticket assignments (Many-to-Many relationship)

Authenticated customer access using JWT

TECH STACK:

Flask

Flask-SQLAlchemy

SQLAlchemy (DeclarativeBase)

Flask-Marshmallow

Swagger UI (API documentation and interactive testing)

unittest (Python standard library for testing)

Flask-JWT-Extended (JWT authentication)

Flask-Caching (performance optimization)

Flask-Limiter (rate limiting and abuse protection)

Application Factory Pattern

Blueprint Architecture

Project Structure
mechanic_shop_api/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── util.py        # contains encode_token function
│   │
│   ├── customer/
│   │   ├── __init__.py
│   │   ├── routes.py     # includes register/login with JWT
│   │   └── schemas.py
│   │
│   ├── mechanic/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── service_ticket/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── inventory/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│
├── tests/
│   ├── __init__.py
│   ├── test_customers.py
│   ├── test_mechanics.py
│   ├── test_service_tickets.py
│   └── test_inventory.py
│
├── config.py
├── run.py
└── requirements.txt
DATABASE MODELS:

Customer:

id (Primary Key)

name

email

phone

password (hashed)

One-to-Many → Service Tickets

Mechanic:

id (Primary Key)

name

email

phone

salary

Many-to-Many → Service Tickets

Service Ticket:

id (Primary Key)

vin

service_date

service_desc

customer_id (Foreign Key)

Many-to-Many → Mechanics

Many-to-Many → Inventory

Inventory:

id (Primary Key)

name

description

price

quantity

Many-to-Many → Service Tickets

Junction Tables:

service_mechanics

ticket_id (Foreign Key)

mechanic_id (Foreign Key)

service_inventory

ticket_id (Foreign Key)

inventory_id (Foreign Key)

Setup Instructions
Clone the Repository
git clone https://github.com/your-username/mechanic-shop-api.git
cd mechanic-shop-api
Create Virtual Environment:

Mac / Linux:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt

If you don't have a requirements file yet:

pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy flask-jwt-extended flask-caching flask-limiter

Then generate it:

pip freeze > requirements.txt
Configure Environment Variables

Create a .env file or configure inside config.py:

SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic_shop.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = "your-secret-key"

# Caching (simple example)
CACHE_TYPE = "SimpleCache"
CACHE_DEFAULT_TIMEOUT = 300
Initialize the Database
flask shell
from app import create_app
from app.models import db

app = create_app()
app.app_context().push()
db.create_all()
Run the Application
flask run

OR

python run.py

Server will run at:

http://127.0.0.1:5000
API Documentation (Swagger UI)

Swagger UI has been integrated to provide interactive API documentation.

Access it at:

http://127.0.0.1:5000/swagger
Authentication (JWT)

JWT authentication is implemented for protected routes such as customer registration and login.

Tokens are generated using the encode_token function located in:

app/utils/util.py

After login, include the token in requests:

Authorization: Bearer <your_token>
Caching

Caching is implemented using Flask-Caching to improve performance on frequently accessed endpoints.

Reduces database load

Speeds up repeated requests

Configurable via config.py

Rate Limiting

Rate limiting is implemented using Flask-Limiter to prevent abuse and ensure API stability.

Limits repeated requests from the same client

Protects endpoints from being overwhelmed

Configurable per route or globally

API Endpoints
Mechanic Routes

URL Prefix: /mechanics

POST /

GET /

PUT /<int:id>

DELETE /<int:id>

Service Ticket Routes

URL Prefix: /service-tickets

POST /

GET /

PUT /assign-mechanic/<mechanic_id>

PUT /remove-mechanic/<mechanic_id>

PUT /add-inventory/<inventory_id>

PUT /remove-inventory/<inventory_id>

Customer Routes

URL Prefix: /customers

POST /register

POST /login

GET /

PUT /<int:id>

DELETE /<int:id>

Inventory Routes

URL Prefix: /inventory

POST /

GET /

PUT /<int:id>

DELETE /<int:id>

Key Concepts Implemented
Application Factory Pattern

App created using create_app()

Blueprints registered in app/__init__.py

Blueprint Architecture

Each resource contains:

routes.py

schemas.py

SQLAlchemy Relationships

One-to-Many (Customer → Service Tickets)

Many-to-Many (Mechanics ↔ Service Tickets)

Many-to-Many (Inventory ↔ Service Tickets)

Authentication

JWT-based authentication

Token generation via encode_token

Protected routes using JWT

Performance Optimization

Flask-Caching for improved response times

Reduced redundant database queries

API Protection

Flask-Limiter for rate limiting

Prevents excessive or abusive requests

Marshmallow Schemas

SQLAlchemyAutoSchema used

Handles serialization and validation

Testing

Testing is implemented using Python’s built-in unittest module.

Tests are located in:

tests/

Run tests with:

python -m unittest discover tests
Testing the API

You can test the API using:

Swagger UI (recommended)

Postman

Thunder Client

curl

Insomnia

Example:

curl http://127.0.0.1:5000/mechanics/