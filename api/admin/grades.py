from ..utils import db
from functools import wraps
from flask import request
from flask_restx import Resource, fields, Namespace
from ..auth.views import generate_random_string, generate_password
from ..models.user import Student, User, Tutor
from ..models.courses import Course, StudentCourse, Score
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies



grade_namespace = Namespace('score', description = 'Student accessible route')


score_model = grade_namespace.model(
    'Score', {
        'student_id': fields.String(required=True, description="Student's First Name"),
        'course_id': fields.String(required=True, description="'Student's Last Name"),
        'score': fields.String(required=True, description="Studend ID")
    }
)

student_score = grade_namespace.model('StudentScores', {
    'course_id': fields.Integer(required=True, description="Course ID"),
    'score': fields.Integer(required=True, description="Student's Score")
})



student_model = grade_namespace.model(
    'Student', {
		'id': fields.String(required=True),
        'first_name': fields.String(required=True, description="Student's First Name"),
        'last_name': fields.String(required=True, description="'Student's Last Name"),
        'email': fields.String(required=True, description="Student's Email"),
		'student_id': fields.String(required=True, description="Studend ID"),
		'password': fields.String(required=True, default="Student101", description="Student's Password"),
        # 'registered_courses': fields.List(fields.Nested(course_list_model)),
		'gpa': fields.String( required=True, description='Student gpa')
        
	}
)






grade_list_model = grade_namespace.model(
    'ScoreView', {
        'id': fields.String(required=True, description="'User's Name"),
        'student_id': fields.String(required=True, description="Student's First Name"),
        'course_id': fields.String(required=True, description="'Student's Last Name"),
        'score': fields.String(required=True, description="Studend ID"),
        'course_name': fields.String(required=True, description="Studend ID")
    }
)


@grade_namespace.route('/course/<int:course_id>/student/<int:student_id>')
class UploadStudentScoreForCourse(Resource):
        
        @grade_namespace.expect(student_score)
        @grade_namespace.marshal_with(score_model)
        @grade_namespace.doc(
            description='Upload a student score for a course'
        )
        @jwt_required()
        def post(self, student_id: int, course_id: int):
            """
                Upload a student score for a course
            """
            data = grade_namespace.payload
            name = get_jwt_identity()

            student = Student.query.filter_by(id=student_id).first()

            if not student:
                grade_namespace.abort(HTTPStatus.NOT_FOUND, message="Student not found")

            course = Course.query.filter_by(id=course_id).first()

            if not course:
                grade_namespace.abort(HTTPStatus.NOT_FOUND, message="Course not found")

            grade  = Score.query.filter_by(student_id=student_id, course_id=course_id).first()

            if grade:
                grade_namespace.abort(HTTPStatus.CONFLICT, message="Grade already uploaded")

            new_grade = Score(
                student_id=student_id,
                course_id=course_id,
                score=data['score']
            )

            new_grade.save()

            return new_grade, HTTPStatus.CREATED

        
