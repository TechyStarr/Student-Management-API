from ..utils import db
from functools import wraps
from flask import request, abort
from flask_restx import Resource, fields, Namespace
from ..admin.views import student_model, create_course_model, student_course_model
from ..auth.views import generate_random_string, generate_password
from ..models.user import Student, User
from ..models.courses import Course, StudentCourse, calculate_grade_points, calculate_gpa, calculate_grades
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


def calculate_grades(score):
    if score >= 70:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 45:
        return 'D'
    elif score >= 40:
        return 'E'
    else:
        return 'F'



student_score_model = grade_namespace.model(
    'StudentScore', {
        'student_id': fields.String(required=True, description="'Student's Last Name"),
        'score': fields.String(required=True, description="Studend ID")
    }
)



@grade_namespace.route('/student/<int:student_id>/courses')
class GetStudentCourses(Resource):
    @grade_namespace.marshal_with(student_course_model)
    @grade_namespace.doc(
        description='Get all courses a student registered for', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    @is_admin
    def get(self, student_id):
        """
            Get all the courses a student registered for
        """
        student = Student.query.filter_by(id=student_id).first()
        if student is None:
            return {
            'message': 'This student does not exist'
                }, HTTPStatus.BAD_REQUEST
        else:
            return student.registered_courses, HTTPStatus.OK
    









    
# @grade_namespace.route('/student/<int:student_id>/scores')
# class StudentScore(Resource):
#     # @grade_namespace.marshal_with(student_score_model)
#     @grade_namespace.doc(
#         description='Get all scores', params={
#             'student_id': 'The student id'
#         }
#     )
#     @jwt_required()
#     @is_admin
#     def get(self, student_id):
#         """
#             Get all scores
#         """
        
#         student_courses = StudentCourse.query.filter_by(student_id=student_id).all()
#         if not student_courses:
#             return {
#                 'message': "This student wasn't registered for any course"
#             }, HTTPStatus.BAD_REQUEST
#         student_id = [student_course.student_id for student_course in student_courses]
#         first_name = [student_course.first_name for student_course in student_courses]
#         course_code = [student_course.course_code for student_course in student_courses]
#         credits = [student_course.course_unit for student_course in student_courses]
#         scores = [student_course.score for student_course in student_courses]
#         grades = []
#         for score in scores:
#             grade = calculate_grades(score)
#             grades.append(grade)

#         courses = []

#         for i in range(len(scores)):
#             score = scores[i]

#             if score >= 70:
#                 grades =  'A'  
#             elif score >= 60:
#                 grades =  'B'  
#             elif score >= 50:
#                 grades =  'C'  
#             elif score >= 45:
#                 grades =  'D'  
#             elif score >= 40:
#                 grades =  'E'  
#             else:
#                 grades =  'F'  

#             course = {
#                 'student_id': student_id[i],
#                 'first_name': first_name[i],
#                 'course_code': course_code[i],
#                 'credits': credits[i],
#                 'score': scores[i],
#                 'grade': grades[:1]
#             }

#             courses.append(course)


#         return courses, HTTPStatus.OK
    

@grade_namespace.route('/student/<int:student_id>/scores')
class CalculateGPA(Resource):
    # @grade_namespace.marshal_with(student_score_model)
    @grade_namespace.doc(
        description='Get all scores', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    @is_admin
    def get(self, student_id):
        """
            Calculate GPA
        """
        
        student_courses = StudentCourse.query.filter_by(student_id=student_id).all()
        if not student_courses:
            return {
                'message': "This student wasn't registered for any course"
            }, HTTPStatus.BAD_REQUEST
        credits = [student_course.course_unit for student_course in student_courses]
        scores = [student_course.score for student_course in student_courses]
        grades = []
        for score in scores:
            grade = calculate_grades(score)
            grades.append(grade)

        total_grade_points = 0.0
        total_credit_units = 0.0

        for i in range(len(grades)):
            if grades[i] == 'A':
                total_grade_points += 5 * credits[i]
                total_credit_units += credits[i]
            elif grades[i] == 'B':
                total_grade_points += 4 * float(credits[i])
                total_credit_units += credits[i]
            elif grades[i] == 'C':
                total_grade_points += 3 * credits[i]
                total_credit_units += credits[i]
            elif grades[i] == 'D':
                total_grade_points += 2 * credits[i]
                total_credit_units += credits[i]
            elif grades[i] == 'E':
                total_grade_points += 1 * credits[i]
                total_credit_units += credits[i]
            elif grades[i] == 'F':
                total_grade_points += 0 * credits[i]
                total_credit_units += credits[i]
        gpa = total_grade_points / total_credit_units

        if gpa >= 4.5:
            response = {
                'message': 'Congratulations, You have been awarded a First Class Honours',
                'gpa': f"Your GPA is {round(gpa, 2)}"
            }
        elif gpa >= 3.5:
            response = {
                'message': 'Congratulations, You have been awarded a Second Class Upper Division',
                'gpa': f"Your GPA is {round(gpa, 2)}"
            }
        elif gpa >= 2.5:
            response = {
                'message': 'Congratulations, You have been awarded a Second Class Lower Division',
                'gpa': f"Your GPA is {round(gpa, 2)}"
            }
        elif gpa >= 1.5:
            response = {
                'message': 'Congratulations, You have been awarded a Third Class',
                'gpa': f"Your GPA is {round(gpa, 2)}"
            }
        else:
            response = {
                'message': 'Sorry, You have been awarded a Pass',
                'gpa': f"Your GPA is {round(gpa, 2)}"
            }
        return response, HTTPStatus.OK





@grade_namespace.route('/student/courses/<int:course_id>')
class GetCourseStudent(Resource):
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



