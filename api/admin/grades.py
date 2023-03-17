from ..utils import db
from functools import wraps
from flask import request
from flask_restx import Resource, fields, Namespace
from ..auth.views import generate_random_string, generate_password
from ..models.user import Student, User, Tutor
from ..models.courses import Course, StudentCourse, Score
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies



score_namespace = Namespace('score', description = 'Student accessible route')


score_model = score_namespace.model(
    'Score', {
        'id': fields.String(required=True, description="'User's Name"),
        'student_id': fields.String(required=True, description="Student's First Name"),
        'course_id': fields.String(required=True, description="'Student's Last Name"),
        'score': fields.String(required=True, description="Studend ID")
    }
)

grade_list_model = score_namespace.model(
    'ScoreView', {
        'id': fields.String(required=True, description="'User's Name"),
        'student_id': fields.String(required=True, description="Student's First Name"),
        'course_id': fields.String(required=True, description="'Student's Last Name"),
        'score': fields.String(required=True, description="Studend ID"),
        'course_name': fields.String(required=True, description="Studend ID")
    }
)




