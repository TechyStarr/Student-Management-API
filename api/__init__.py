from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .admin.views import admin_namespace
from .students.views import course_namespace
from .admin.grades import grade_namespace
from .config.config import config_dict
from .utils import db
from .models.courses import Course
from .models.user import User, Student, Tutor
from .models.courses import Course, StudentCourse, Score
from flask_migrate import Migrate
# from flask_script import Manager
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed
from redis import Redis



def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)


    redis_blocklist = Redis(host='localhost', port=6379, db=0, decode_responses=True)

    # @jwt.token_in_blocklist_loader
    # def check_if_token_revoked(jwt_header, jwt_payload):
    #     jti = jwt_payload['jti']
    #     token_in_blocklist = redis_blocklist.get(jti)
    #     return token_in_blocklist is not None


    migrate = Migrate(app, db)
    # manager = Manager(app)

    # manager.add_command('db')

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
            description='A student management API for managing student records with provided access to admin and students',
            authorizations=authorizations,
            security="Bearer Auth"
            )
            


    api.add_namespace(auth_namespace)
    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(grade_namespace, path='/grades')
    
    

    @app.shell_context_processor 
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Student': Student,
            'Tutor': Tutor,
            'Course': Course,
            'StudentCourse': StudentCourse,
            'Score': Score
        }


    return app