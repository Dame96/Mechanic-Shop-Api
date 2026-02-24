
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List


# create a base class which inherits its properties from"DelclarativeBase" class that was imported from the sqlalchemy.orm package. 
class Base(DeclarativeBase):
    pass

# instanciating SQLAlchemy Datbase with this base class and make that the model class
# any class that inherits this base class will be one of my database's models. 
db = SQLAlchemy(model_class = Base)



# Creating Database Tables, interiting from the Base(DeclarativeBase) class, this way its registered as a Database table in our configured database.
# attributes/properties - are the fields/columns in the table(model).
#==== TABLES =========
#== Junction Table ==# 

service_mechanics = db.Table(
     'service_mechanics', 
    Base.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'), primary_key=True)
)


class Customer(Base):
     __tablename__ = 'customers'

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(db.String(255), nullable=False)
     email: Mapped[str] = mapped_column(db.String(360), nullable=False)
     phone: Mapped[str] = mapped_column(db.String(15), nullable=False)

     service_tickets: Mapped[List['Service_Ticket']] = db.relationship(back_populates='customer')

class Service_Ticket(Base):
     __tablename__ = 'service_tickets'

     id: Mapped[int] = mapped_column(primary_key=True)
     vin: Mapped[str] = mapped_column(db.String(200), nullable=False)
     service_date: Mapped[str] = mapped_column(db.String(200), nullable=False)
     service_desc: Mapped[str] = mapped_column(db.String(250), nullable=False)
     customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
     
     mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_mechanics, back_populates='service_tickets') # secondary tells SQLalchemy to use the association table
     customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')

class Mechanic(Base):
     __tablename__ = 'mechanics'

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(db.String(255), nullable=False)
     email: Mapped[str] = mapped_column(db.String(360), nullable=False)
     phone: Mapped[str] = mapped_column(db.String(15), nullable=False)
     salary: Mapped[float] = mapped_column(db.Float, nullable=False)

     service_tickets: Mapped[List['Service_Ticket']] = db.relationship(secondary=service_mechanics, back_populates='mechanics') 