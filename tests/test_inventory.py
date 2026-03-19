from app import create_app 
from app.models import db, Inventory 
import unittest 

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig") # create the test app
        self.inventory = Inventory(name="Engine", price=3000.00) #create a model instance 

        with self.app.app_context(): # Use the application context for DB operations
            db.drop_all() # resetting the database
            db.create_all() 
            db.session.add(self.inventory) #insert test data
            db.session.commit() 

        self.client = self.app.test_client() # create a test client


    
    def test_create_inventory(self):
        inventory_payload = {
            "name": "Bumper",
            "price": 750.00
        }

        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Bumper")


    def test_get_inventory(self):
        response = self.client.get('/inventory/')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)


    def test_update_inventory(self):

        with self.app.app_context():
            inventory = Inventory(name="Transmission", price=2000.00)
            db.session.add(inventory)
            db.session.commit()
            inventory_id = inventory.id

        update_payload = {
            "name": "Front-Bumper",
            "price": 1000.00
        }

        response = self.client.put(f'/inventory/{inventory_id}', json=update_payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Front-Bumper")
        self.assertEqual(response.json['price'], 1000.00)



    def test_delete_inventory(self):

        with self.app.app_context():
            inventory = Inventory(name="tire", price=350.00)
            db.session.add(inventory)
            db.session.commit()
            inventory_id = inventory.id 


        response = self.client.delete(f'/inventory/{inventory_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], f"Part ID: {inventory_id}, successfully deleted from inventory records.")

