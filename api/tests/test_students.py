import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.user import User, Student
from flask_jwt_extended import create_access_token


class StudentTestCase(unittest.TestCase):
    
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


    
    # Create a student/
    def test_create_a_student(self):
        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            'student_id': 'ALT00198',
            'email': 'john@email.com',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = self.client.post('/Admin/students', json=data, headers=headers)
        assert response.status_code == 201

        # students = Student.query.all()
        # student_id = students.student.id
        # assert student_id == 'ALT00198'
        # assert response.json == {
        #     'student_id': 'ALT00198',
        #     'email': 'john@email',
        #     'first_name': 'John',
        #     'last_name': 'Doe',
        # }



    # Retrieve all students
    def test_get_all_students(self):
        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        


        response = self.client.get('/Admin/students', headers=headers)

        assert response.status_code == 201


    # Retrieve a student
    def test_get_a_student(self):
        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/Admin/students/ALT00198', headers=headers)

        assert response.status_code == 200


    def test_create_a_student(self, client, admin_headers):
    # create test data
        data = {
            "email": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }

        # make API call
        response = client.post("/students", headers=admin_headers, json=data)

        # assert response status code and message
        assert 201 == response.status_code
        assert "Student created successfully" == response.json["message"]




