from ..utils import db
from flask import request
from flask_restx import Resource, fields, Namespace
from ..auth.views import generate_random_string, generate_password
from ..models.user import Student, User, Tutor
from ..models.courses import Course, StudentCourse
from ..auth.views import generate_random_string, generate_password, login_model
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from redis import Redis


course_namespace = Namespace('course', description = 'Student accessible route')



course_model = course_namespace.model(
    'Student', {
		'id': fields.String(required=True, description="'User's Name"),
        'first_name': fields.String(required=True, description="Student's First Name"),
        'last_name': fields.String(required=True, description="'Student's Last Name"),
		'student_id': fields.String(required=True, description="Studend ID"),
		'password': fields.String(required=True, default="Student101", description="Student's Password")
        
	}
)


student_course_model = course_namespace.model(
    'StudentCourse', {
        'id': fields.String(required=True, description="'User's Name"),
        'course_id': fields.String(required=True, description="Student's First Name"),
        'student_id': fields.String(required=True, description="'Student's Last Name"),
        'grade': fields.String(required=True, description="Studend ID")
    }
)


# student_course_code





# Retrieve the student from the database using student_id/matric no
# Use the student's login details to autheticate the request
# Create a new course oject with the given data
# Add the course to the student's courses list
# Save the changes to the database


@course_namespace.route('/student/<int:student_id>')
class ResetPassword(Resource):

    @course_namespace.marshal_with(login_model)
    @course_namespace.doc(
        description='Reset student password', params={
            'student_id': 'The student id'
        }
    )
    def post(self, student_id):
        """
            Reset student password
        """
        pass


@course_namespace.route('student/<int:student_id>/courses')
class GetStudentCourses(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Get all scores for all courses a student registered for', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Get all scores for a student
        """
        student = Student.get_by_id(student_id)
        if student is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        else:
            return student.registered_courses, HTTPStatus.OK




@course_namespace.route('/students/<int:student_id>/courses')
class GetStudents(Resource):
    
    @course_namespace.marshal_with(student_course_model, as_list=True)
    @course_namespace.doc(
        description='Get all courses registered to a student',
    )
    @jwt_required()
    def get(self, student_id):
        """
            Retrieve all courses registered to a student
        """

        current_user = Student.get_by_id(student_id)

        student = get_jwt_identity()
        if student:
            courses = StudentCourse.query.all()
            return courses, HTTPStatus.OK
        return {
            'message': 'No students found'
        }



@course_namespace.route('/student')
class RetrieveStudentCourses(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Get all scores for all courses a student registered for', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    def get(self):
        """
            Get all scores for a 
        """
        student = Student.get_by_id(get_jwt_identity())
        if student is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        else:
            return student.registered_courses, HTTPStatus.OK


    

@course_namespace.route('/student/<int:student_id>')
class CalculateGPA(Resource):
    
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Retrieve a student GPA by current_student/jwt_identity', params={
            'student_id': 'The student id'
        }
    )
    def get(self, student_id):
        """
            Retrieve a student GPA by current_student/jwt_identity
        """

        student = Student.get_by_id(student_id)
        if student is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        else:  
            
            # Calculate GPA
            # gpa = 0
            # for course in student.registered_courses:
            #     gpa += course.grade
            # gpa = gpa / len(student.registered_courses)
            # student.gpa = gpa
            # student.save()
            


            return student, HTTPStatus.OK
        


    