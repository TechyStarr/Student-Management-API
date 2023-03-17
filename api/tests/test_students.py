import unittest
from ..import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.user import User
from flask_jwt_extended import create_access_token


class OrderTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context() # Creates the db

        self.appctx.push()
        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self): # teardown resets existing tables in the database
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    # Get all orders
    def test_get_all_orders(self):
        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }


        response = self.client.get('/Order/orders', headers=headers)

        assert response.status_code == 200

        assert response.json == []

    
    # Place an order
    def test_place_an_order(self):

        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        
        data = {
            "size": "LARGE",
            "quantity": "16",
            "flavour": "chicken"
        }
        response = self.client.post('/Order/orders', headers = headers, json=data)

        assert response.status_code == 201

        orders = Order.query.all()

        order_id = orders[0].id

        assert order_id == 1
        
        assert len(orders) == 1
        assert response.json['size'] == 'Sizes.LARGE'

    
    # Get an order by Id
    def test_get_single_order(self):
        token = create_access_token(identity="Test User")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/orders/order/1', headers=headers)

        assert response.status_code == 404

        

    # Update an order
    def test_update_order(self):
        token = create_access_token(identity="testuser")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "size": "LARGE",
            "quantity": "4",
            "flavour": "pepperoni"
        }

        response = self.client.post('/Order/order/1', headers=headers, json=data)
