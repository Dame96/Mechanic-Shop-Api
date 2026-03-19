from app import create_app 
from app.models import db, Customer, Service_Ticket
from app.utils.util import encode_token 
import unittest 

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="test_user", email="test@email.com", password="test", phone="1234567890")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()


    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "password": "123",
            "phone": "1234567890"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")


    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])


    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn("auth_token", data)
    

    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['messages'], 'Invalid email or password')



    def test_update_customer(self):

        login = self.client.post('/customers/login', json={
            "email": "test@email.com",
            "password": "test"
        })

        token = login.get_json()["auth_token"]

        headers = {'Authorization': f"Bearer {token}"}

        update_payload = {
            "name": "Peter",
            "phone": "1234567890",
            "email": "test@email.com",
            "password": "test"
        }
        response = self.client.put('/customers/', json=update_payload, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter')
        self.assertEqual(response.json['email'], 'test@email.com')



    def test_get_customers(self):
        response = self.client.get('/customers/')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)


    def test_get_customer(self):
        with self.app.app_context():
            customer = Customer(name="John Doe", email="john@test.com", password="password123", phone="1234567890")
            db.session.add(customer)
            db.session.commit()
            customer_id = customer.id 

        response = self.client.get(f'/customers/{customer_id}')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["id"], customer_id)
        self.assertEqual(data["name"], "John Doe")


    def test_get_customer_not_found(self):
        response = self.client.get('/customers/9999')

        self.assertEqual(response.status_code, 404)

        data = response.get_json()

        self.assertEqual(data["error"], "Customer not found.")


    def test_get_customer_tickets(self):
        #login to get token 
        login = self.client.post('/customers/login', json={
            "email": "test@email.com",
            "password": "test"
        })

        token = login.get_json()["auth_token"]

        headers = {
            "Authorization": f"Bearer {token}"
        }

        #create service tickets for this customer
        with self.app.app_context():
            ticket1 = Service_Ticket(
                service_desc="Oil change",
                vin="123ABC",
                customer_id=1, 
                service_date="12-25-1996"
            )

            ticket2 = Service_Ticket(
                service_desc="Brake repair",
                vin="456DEF",
                customer_id=1,
                service_date="12-25-1996"
            )

            db.session.add_all([ticket1, ticket2])
            db.session.commit()

        response = self.client.get('/customers/my-tickets', headers=headers)


        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        #verify the number of tickets
        self.assertEqual(len(data), 2)

        #extract descriptions
        services = [ticket["service_desc"] for ticket in data]

        #check that both services exist 
        self.assertIn("Oil change", services)
        self.assertIn("Brake repair", services)



    def test_delete_customer(self):
        
        # login to get token
        login = self.client.post('/customers/login', json={
            "email": "test@email.com",
            "password": "test"
        })

        token = login.get_json()["auth_token"]

        headers = {
            "Authorization": f"Bearer {token}"
        }

        #send delete request
        response = self.client.delete('/customers/', headers=headers)

        self.assertEqual(response.status_code, 200) # check that the response code 200 confirms that successful deletion 

        data = response.get_json()

        self.assertEqual(
            data["message"], 
            "Customer id: 1, successfully deleted."
        )

        #verify customer was removed from the DB
        with self.app.app_context():
            customer = db.session.get(Customer,1)
            self.assertIsNone(customer) 