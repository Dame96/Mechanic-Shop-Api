# Mechanic-Shop-Api


A RESTful API built with Flask, SQLAlchemy, Marshmallow, and the Application Factory Pattern** to manage a mechanic shop system.

This API allows you to manage:

* Customers
* Mechanics
* Service Tickets
* Mechanic ↔ Service Ticket assignments (Many-to-Many relationship)

---

Tech Stack

* Flask
* Flask-SQLAlchemy
* SQLAlchemy (DeclarativeBase)
* Flask-Marshmallow
* Application Factory Pattern
* Blueprint Architecture

---

Project Structure

```
mechanic_shop_api/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   │
│   ├── customer/
│   │   ├── __init__.py
│   │   ├── routes.py
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
│
├── config.py
├── run.py
└── requirements.txt
```

---

Database Models

Customer

* id (Primary Key)
* name
* email
* phone
* One-to-Many → Service Tickets

Mechanic

* id (Primary Key)
* name
* email
* phone
* salary
* Many-to-Many → Service Tickets

Service Ticket

* id (Primary Key)
* vin
* service_date
* service_desc
* customer_id (Foreign Key)
* Many-to-Many → Mechanics

Junction Table

`service_mechanics`

* ticket_id
* mechanic_id

---

Setup Instructions

Clone the Repository

```bash
git clone https://github.com/your-username/mechanic-shop-api.git
cd mechanic-shop-api
```

---

Create Virtual Environment

Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements file yet:

```bash
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy
```

Then generate it:

```bash
pip freeze > requirements.txt
```

---

Configure Environment Variables

Create a `.env` file or configure inside `config.py`:

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic_shop.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

Initialize the Database

If using Flask shell:

```bash
flask shell
```

```python
from app import create_app
from app.models import db

app = create_app()
app.app_context().push()
db.create_all()
```

---

Run the Application

```bash
flask run
```

OR

```bash
python run.py
```

Server will run at:

```
http://127.0.0.1:5000
```

---

API Endpoints

---

Mechanic Routes

URL Prefix:** `/mechanics`

Create Mechanic

```
POST /mechanics/
```

Body Example:**

```json
{
  "name": "John Doe",
  "email": "john@email.com",
  "phone": "5551234567",
  "salary": 60000
}
```

---

Get All Mechanics

```
GET /mechanics/
```

---

Update Mechanic

```
PUT /mechanics/<int:id>
```

---

Delete Mechanic

```
DELETE /mechanics/<int:id>
```

---

Service Ticket Routes

URL Prefix:** `/service-tickets`

---

Create Service Ticket

```
POST /service-tickets/
```

Body Example:**

```json
{
  "vin": "1HGCM82633A123456",
  "service_date": "2026-02-24",
  "service_desc": "Oil Change",
  "customer_id": 1
}
```

---

Assign Mechanic to Service Ticket

```
PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>
```

---

Remove Mechanic from Service Ticket

```
PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>
```

---

Get All Service Tickets

```
GET /service-tickets/
```

---

Customer Routes

URL Prefix:** `/customers`

(Previously implemented)

* POST `/`
* GET `/`
* PUT `/<int:id>`
* DELETE `/<int:id>`

---

 Key Concepts Implemented

Application Factory Pattern

* App created using `create_app()`
* Blueprints registered inside `app/__init__.py`

Blueprint Architecture

Each resource has:

* `__init__.py`
* `routes.py`
* `schemas.py`

SQLAlchemy Relationships

* One-to-Many (Customer → Service Tickets)
* Many-to-Many (Mechanics ↔ Service Tickets)
* Junction table: `service_mechanics`

Marshmallow Auto Schemas

* Used `SQLAlchemyAutoSchema`
* Handles serialization and validation

---

Testing the API

Use:

* Postman
* Thunder Client (VS Code)
* curl
* Insomnia

Example:

```bash
curl http://127.0.0.1:5000/mechanics/
```



