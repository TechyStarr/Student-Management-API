from ..utils import db
from flask import request
from flask_restx import Resource, fields, Namespace
from ..admin.views import student_model, create_course_model, student_course_model
from ..auth.views import generate_random_string, generate_password
from ..models.user import Student, User
from ..models.courses import Course, StudentCourse
from ..auth.views import generate_random_string, generate_password, login_model
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from redis import Redis


student_namespace = Namespace('Student', description = 'Student accessible route')






student_score_model = student_namespace.model(
    'StudentScore', {
        'id': fields.String(required=True, description="'User's Name"),
        'course_id': fields.String(required=True, description="Student's First Name"),
        'student_id': fields.String(required=True, description="'Student's Last Name"),
        'grade': fields.String(required=True, description="Studend ID")
    }
)


# student_course_code





@student_namespace.route('/student/updateprofile/<int:student_id>')
class StudentProfile(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Update student profile'
    )
    @jwt_required()
    def patch(self, student_id):
        """
            Update student profile
        """
        data = request.get_json()
        # update_student = Student.get_by_id(student_id)
        student = Student.query.filter_by(id=student_id).first()

        if student is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.email = data['email']
        student.password = data['password']

        student.update()

        return student, HTTPStatus.OK, {
            'message': 'Your profile has been updated successfully'
        }
    


    @student_namespace.marshal_with(login_model)
    @student_namespace.doc(
        description='Reset student password', params={
            'student_id': 'The student id'
        }
    )
    def post(self):
        """
            Reset student password
        """
        pass




@student_namespace.route('/student/<int:student_id>/courses')
class GetStudentCourses(Resource):
    @student_namespace.marshal_with(student_course_model)
    @student_namespace.doc(
        description='Get all courses a student registered for', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Get all courses for a student
        """
        student = Student.query.filter_by(id=student_id).first()
        if student is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        else:
            return student.registered_courses, HTTPStatus.OK
        


@student_namespace.route('/student/<int:student_id>/courses')
class GetCourseStudent(Resource):
    @student_namespace.marshal_with(student_course_model)
    @student_namespace.doc(
        description='Get students registered in a course', params={
            'course_id': 'The course id'
        }
    )
    @jwt_required()
    def get(self, course_id):
        """
            Get all scores for a student
        """
        course = Course.query.filter_by(id=course_id).first()
        if course is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        else:
            return course.student_courses, HTTPStatus.OK




    

@student_namespace.route('/student/<int:student_id>')
class CalculateGPA(Resource):
    
    @student_namespace.marshal_with(student_course_model)
    @student_namespace.doc(
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
        


    