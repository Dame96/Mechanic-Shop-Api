from app import create_app 
from app.models import db, Mechanic, Service_Ticket 
import unittest 


class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig") #create the test app
        self.mechanic = Mechanic(name="MechanicOne", email="mech@email.com", phone="1234567890", salary=100000.00)

        with self.app.app_context(): # Use the app context for DB operations
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic) # insert the test data
            db.session.commit()

        self.client = self.app.test_client() # create a test client

    def test_create_mechanic(self):

        mechanic_payload = {
            "name": "MechanicTwo",
            "email": "mechTwo@email.com",
            "phone": "1234567890",
            "salary": 200000.00
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "MechanicTwo")


    def test_get_mechanics(self):

        response = self.client.get('/mechanics/')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)



    def test_update_mechanic(self):

        with self.app.app_context():
            mechanic = Mechanic(name="MechanicTwo", email="mechtwo@email.com", phone="1234567890", salary=250000.00)
            db.session.add(mechanic)
            db.session.commit()
            mechanic_id = mechanic.id 
        
        update_payload = {
            "name": "MechanicThree",
            "email": "mechthree@email.com",
            "phone": "1234567890",
            "salary": 300000.00
        }


        response = self.client.put(f'/mechanics/{mechanic_id}', json=update_payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "MechanicThree")
        self.assertEqual(response.json['email'], "mechthree@email.com")


    def test_delete_mechanic(self):
        with self.app.app_context():
            mechanic = Mechanic(name="MechanicFour", email="mechfour@email.com", phone="1234567890", salary=100000.00)
            db.session.add(mechanic)
            db.session.commit()
            mechanic_id = mechanic.id 

        response = self.client.delete(f'mechanics/{mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], f"Mechanic id: {mechanic_id}, successfully deleted.")


    def test_popular_mechanics(self):

        with self.app.app_context():
            # Create mechanics
            mech1 = Mechanic(name="MechanicTwo", email="one@email.com", phone="1234567890", salary=100000)
            mech2 = Mechanic(name="MechanicThree", email="two@email.com", phone="1234567890", salary=200000)

            db.session.add_all([mech1, mech2])
            db.session.commit()

            # Create a service tickets
            ticket1 = Service_Ticket(vin="fbeo8ty33437gd", service_date="12-25-2013", service_desc="engine replacement", customer_id=1)
            ticket2 = Service_Ticket(vin="h43908f399h", service_date="01-31-2025", service_desc="tire repalcements", customer_id=2)
            ticket3 = Service_Ticket(vin="fh304923hbr29", service_date="07-25-1996", service_desc="windshiled replacement", customer_id=3)

            db.session.add_all([ticket1, ticket2, ticket3])
            db.session.commit()

        response = self.client.get('/mechanics/popular')

        self.assertEqual(response.status_code, 200)

        data = response.json 

        self.assertEqual(data[0]['name'], "MechanicOne")
        self.assertEqual(data[1]['name'], "MechanicTwo")



    def test_search_mechanic(self):
        with self.app.app_context():
            mech2 = Mechanic(name="JohnMechanic", email="john@email.com", phone="1234567890", salary=50000)
            mech3 = Mechanic(name="MikeMechanic", email="mike@email.com", phone="0987654321", salary=75000)

            db.session.add_all([mech2, mech3])
            db.session.commit()

        # Search for Mechanic
        response = self.client.get('/mechanics/search?name=Mechanic')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        # Should return matches containing "Mechanic"
        self.assertTrue(len(data) >= 1)

        # Check that the returned names contain the search term
        for mech in data:
            self.assertIn("Mechanic", mech['name'])

        