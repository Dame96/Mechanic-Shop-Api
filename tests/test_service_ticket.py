from app import create_app 
from app.models import db, Mechanic, Service_Ticket, Inventory 
import unittest 


class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig") # create the test app
        self.ServiceTicket = Service_Ticket(vin="her39r3903r5", service_date="03-26-1999", service_desc="engine repalcement", customer_id=1)

        with self.app.app_context(): # Use the app context for DB operations
            db.drop_all()
            db.create_all()
            db.session.add(self.ServiceTicket) # insert the test data
            db.session.commit()

            self.service_ticket_id = self.ServiceTicket.id
        self.client = self.app.test_client() #create a test client

    def test_create_service_ticket(self):

        ServiceTicket_Payload = {
            "vin": "bfe93r3f32r0h", 
            "service_date": "12-25-2012",
            "service_desc": "front bumper replacement", 
            "customer_id": 2
        }

        response = self.client.post('/service-tickets/', json=ServiceTicket_Payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['vin'], "bfe93r3f32r0h")


    def test_get_service_tickets(self):

        response = self.client.get('/service-tickets/')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)



    def test_assign_inventory_to_service_ticket(self):

        with self.app.app_context():
            # Create inventory item
            inventory_item = Inventory(
                name="Brake Pad", 
                price=200
            )

            db.session.add(inventory_item)
            db.session.commit()

            
            inventory_id = inventory_item.id 


        # Call the route 
        response = self.client.put(
            f'/service-tickets/{self.service_ticket_id}/assign-inventory/{inventory_id}'
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIn("added to service ticket", data['message'])



    def test_assign_mechanic_to_service_ticket(self):

        with self.app.app_context():
            # Create a mechanic
            mechanic = Mechanic(
                name="Test Mechanic", 
                email="test@email.com",
                phone="1234567890",
                salary=75000
            )

            db.session.add(mechanic)
            db.session.commit()

            mechanic_id = mechanic.id 
        
        response = self.client.put(f'/service-tickets/{self.service_ticket_id}/assign-mechanic/{mechanic_id}')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIn("assigned to service ticket", data['message'])
            
            

    def edit_service_ticket_mechanics(self):

        with self.app.app_context():
            # Creating Mechanics
            mech1 = Mechanic(
                name="Mechanic One",
                email="one@email.com",
                phone="113939993",
                salary=100000
            )
            mech2 = Mechanic(
                name="Mechanic Two",
                email="two@email.com",
                phone="2292939939",
                salary=90000
            )

            db.session.add_all([mech1, mech2])
            db.session.commit()

            mech1_id = mech1.id 
            mech2_id = mech2.id 

            # Assing mech1 initially (so we can test removal)
            service_ticket = db.session.get(Service_Ticket, self.service_ticket_id)
            service_ticket.mechanics.append(mech1)
            db.session.commit()

        payload = {
            "add_mechanic_ids": [mech2_id],
            "remove_mechanic_ids": [mech1_id]
        }

        response = self.client.put(f'/service-tickets/{self.service_ticket_id}/edit',json=payload)

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        # Extract mechanic ID's from response
        mechanic_ids = [m['id'] for m in data['mechanics']]

        # mech2 should be added
        self.assertIn(mech2_id, mechanic_ids)

        # mech1 should be removed
        self.assertNotIn(mech1_id, mechanic_ids)


    def test_remove_mechanic_from_service_ticket(self):

        with self.app.app_context():
            # Creating a mechanic
            mechanic = Mechanic(
                name="Test Mechanic",
                email="test@email.com",
                phone="1234567890",
                salary=80000
            )

            db.session.add(mechanic)
            db.session.commit()

            mechanic_id = mechanic.id

            # Assigning mechanic to service ticket first
            service_ticket = db.session.get(Service_Ticket, self.service_ticket_id)
            service_ticket.mechanics.append(mechanic)
            db.session.commit()
        # Removing mechanic
        response = self.client.put(f'/service-tickets/{self.service_ticket_id}/remove-mechanic/{mechanic_id}')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIn("removed from service ticket", data['message'])
