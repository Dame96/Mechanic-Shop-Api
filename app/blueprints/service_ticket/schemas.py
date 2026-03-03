from app.extensions import ma
from app.models import Service_Ticket
from marshmallow import fields 

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket #using the SQLAlchemy model to create fields used in serialization(turning python object into json), deserialization(turning json into python object), and validation(ensuring all required fields are accounted for)
        include_fk = True
        # By default, SQLAlchemyAutoSchema: does NOT include foreign keys unless you specify include_fk = True. This ensures the customer_id field is handled corrected during validation/serialization. 
        

class EditServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")

service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)
return_service_tickets_schema = Service_TicketSchema(exclude=["customer_id"])
edit_service_tickets_schema = EditServiceTicketSchema()