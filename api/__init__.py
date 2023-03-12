from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.courses import Course
from .models.user import User, Admin, Student, Tutor
from .models.courses import Course, StudentCourse, Score
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed



def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)


    api = Api(app)


    api.add_namespace(auth_namespace)
    # api.add_namespace(course_namespace, path='/courses')
    # api.add_namespace(student_namespace, path='/students')
    
    

    @app.shell_context_processor 
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Admin': Admin,
            'Student': Student,
            'Tutor': Tutor,
            'Course': Course,
            'StudentCourse': StudentCourse,
            'Score': Score
        }


    return app