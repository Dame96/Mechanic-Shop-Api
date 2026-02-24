from app.extensions import ma
from app.models import Mechanic


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic #using the SQLAlchemy model to create fields used in serialiation, deserialiation, and validation.


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True) #variant that allows for the serialization of many users
