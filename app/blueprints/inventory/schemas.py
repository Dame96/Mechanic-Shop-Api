from app.extensions import ma
from app.models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory # using the Inventory Model for validation, serialization, deserialization, etc




inventory_schema = InventorySchema()
inventorys_schema = InventorySchema(many=True)