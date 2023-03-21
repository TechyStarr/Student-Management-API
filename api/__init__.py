from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .admin.views import admin_namespace
from .students.views import student_namespace
from .admin.grades import grade_namespace
from .config.config import config_dict
from .utils import db
from .utils.blocklist import BLOCKLIST
from .models.courses import Course
from .models.user import User, Student
from .models.courses import Course, StudentCourse
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed




def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)


    migrate = Migrate(app, db)


    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize user "
        }
    }



    api = Api(app,
            title='Student Management API',
            description='A student management API for managing student records with provided access to admin and students.\n'
            'The API is built with Python, Flask and Flask-RESTX and is still under development.\n'
            'Follow the steps below to use the API:\n'
            '1. Create a user account\n'
            '2. Login to generate a JWT token\n'
            '3. Add the token to the Authorization header with the Bearer prefix eg "Bearer JWT-token"\n'
            '4. Use the token to access the endpoints',

            authorizations=authorizations,
            security="Bearer Auth"
            )


    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 404



    api.add_namespace(auth_namespace)
    api.add_namespace(student_namespace, path='/courses')
    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(grade_namespace, path='/grades')
    
    

    @app.shell_context_processor 
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Student': Student,
            'Course': Course,
            'StudentCourse': StudentCourse,
        }


    return app