from ..utils import db
from functools import wraps
from flask import request, abort
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


grade_namespace = Namespace('Grades', description = 'Student accessible route')


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # check if user is admin
        password = get_jwt_identity()
        if password == 'Student101':
            abort(401, 'You are not authorized to access this route')
        return f(*args, **kwargs)
    return decorated_function


def calculate_grades(self):
    if self.score >= 90:
        return 'A'
    elif self.score >= 80:
        return 'B'
    elif self.score >= 70:
        return 'C'
    elif self.score >= 60:
        return 'D'
    else:
        return 'F'





student_score_model = grade_namespace.model(
    'StudentScore', {
        'id': fields.String(required=True, description="'User's Name"),
        'course_id': fields.String(required=True, description="Student's First Name"),
        'student_id': fields.String(required=True, description="'Student's Last Name"),
        'score': fields.String(required=True, description="Studend ID")
    }
)


# student_course_code






@grade_namespace.route('/student/<int:student_id>/courses')
class GetStudentCourses(Resource):
    @grade_namespace.marshal_with(student_course_model)
    @grade_namespace.doc(
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
        


# @grade_namespace.route('/student/<int:student_id>/courses')
# class GetCourseStudent(Resource):
#     @grade_namespace.marshal_with(student_course_model)
#     @grade_namespace.doc(
#         description='Get students registered in a course', params={
#             'course_id': 'The course id'
#         }
#     )
#     @jwt_required()
#     def get(self, course_id):
#         """
#             Get all scores for a student
#         """
#         course = Course.query.filter_by(id=course_id).first()
#         if course is None:
#             return {
#             'message': 'This student does not exist'
#                 }, HTTPStatus.BAD_REQUEST
#         else:
#             return course.student_courses, HTTPStatus.OK





grade_points = {
    'A': 4,
    'B': 3,
    'C': 2,
    'D': 1,
    'F': 0
}


def calculate_gpa(grades):
    total_grade_points = 0
    for grade in grades:
        total_grade_points += grade_points[grade]
        total_credit += grade['credits']
    return total_grade_points / total_credit








    

@grade_namespace.route('/student/<int:student_id>')
class CalculateGPA(Resource):
    
    @grade_namespace.marshal_with(student_model)
    @grade_namespace.doc(
        description='Calculate a student GPA', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    @is_admin
    def get(self, student_id):
        """
            Calculate a student GPA
        """

        student = Student.get_by_id(student_id)
        if student is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        else:
            
            #Calculate GPA
            gpa = 0
            student = StudentCourse.query.filter_by(id=student_id).first()

            if not student:
                return {
                    'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
            

        score = StudentCourse.query.filter_by(student_id=student_id).all()
        grades = [calculate_grades(score) for score in score]
        gpa = calculate_gpa(grades)
        return {
            'gpa': gpa
        }, HTTPStatus.OK
    

@grade_namespace.route('/student/<int:student_id>/scores')
class StudentScore(Resource):
    @grade_namespace.marshal_with(student_score_model)
    @grade_namespace.doc(
        description='Get all scores', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    @is_admin
    def get(self, student_id):
        """
            Get all scores
        """
        student = StudentCourse.query.filter_by(id=student_id).first()
        if student is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        else:
            for score in StudentCourse:
                return score, {
                    'score': student.score
                }




@grade_namespace.route('/student/<int:student_id>/courses')
class GetCourseStudent(Resource):
    @grade_namespace.marshal_with(student_course_model)
    @grade_namespace.doc(
        description='Get students registered in a course', params={
            'course_id': 'The course id'
        }
    )
    @jwt_required()
    def get(self, course_id):
        """
            Get all scores fo
        """
        scores = []
        course = StudentCourse.query.filter_by(id=course_id).first()
        if course is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        else:
            return course, HTTPStatus.OK
        

    @grade_namespace.expect(student_course_model)
    @grade_namespace.doc(
        description='Update student details in a course', params={ 
            'course_id': 'The course id'
        }
    )
    @jwt_required()
    @is_admin
    def patch(self, course_id):
        """
            Update student details in a course
        """
        student = StudentCourse.query.filter_by(id=course_id).first()
        if student is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        
        #Update student details

        data = grade_namespace.payload
        student.course_code = data['course_code']
        student.course_unit = data['course_unit']
        student.score = data['score']
        student.grade = data['grade']
        student.first_name = data['first_name']
        student.last_name = data['last_name']

        student.save()

        try:
            return student, {
                'message': 'Successfully updated'
            }, HTTPStatus.OK
        except:
            return {
                'message': 'Something went wrong'
            }, HTTPStatus.INTERNAL_SERVER_ERROR







# Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3OTI0NTQ3OCwianRpIjoiZGNlMDdmM2UtOWEwOC00MGJlLWI1MGMtYzllMzU3YjQ3OTRlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InN0YXJyQGVtYWlsIiwibmJmIjoxNjc5MjQ1NDc4LCJleHAiOjE2NzkyNTA4Nzh9.j7TsB-ZAtRuBoOlXNExIE2h-YTuMexcxdkV2yR2BgdE


