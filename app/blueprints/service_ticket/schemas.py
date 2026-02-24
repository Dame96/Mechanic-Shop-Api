from app.extensions import ma
from app.models import Service_Ticket

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket #using the SQLAlchemy model to create fields used in serialization(turning python object into json), deserialization(turning json into python object), and validation(ensuring all required fields are accounted for)
        include_fk = True
        # By default, SQLAlchemyAutoSchema: does NOT include foreign keys unless you specify include_fk = True. This ensures the customer_id field is handled corrected during validation/serialization. 
        

service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)