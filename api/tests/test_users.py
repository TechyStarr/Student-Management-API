import unittest
from ..import create_app
from ..config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.user import Student, Tutor, Admin, User



class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()

        self.appctx.push()
        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test_user@gmail.com',
            'password_hash': 'testpassword',
        }
        response = self.client.post('/auth/register', json=data)

        user = User.query.filter_by(email="test_user@gmail.com").first()

        student = Student.query.filter_by(username=data['username']).first()

        assert response.status_code == 201