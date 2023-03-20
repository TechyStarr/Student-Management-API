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








    
@grade_namespace.route('/student/<int:student_id>/scores')
class StudentScore(Resource):
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
            Get all scores
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

        for i in range(len(scores)):
            score = float(scores[i])

            if score >= 70:
                grades('A')
            elif score >= 60:
                grades('B')
            elif score >= 50:
                grades('C')
            elif score >= 45:
                grades('D')
            elif score >= 40:
                grades('E')
            else:
                grades('F')

            course = {
                'course_code': student_courses[i].course_code,
                'course_unit': student_courses[i].course_unit,
                'score': scores[i],
                'grade': grades[i]
            }


        return course
    

# @grade_namespace.route('/student/<int:student_id>/scores')
# class CalculateGPA(Resource):
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
#             Calculate GPA
#         """
        
#         student_courses = StudentCourse.query.filter_by(student_id=student_id).all()
#         if not student_courses:
#             return {
#                 'message': "This student wasn't registered for any course"
#             }, HTTPStatus.BAD_REQUEST
#         credits = [student_course.course_unit for student_course in student_courses]
#         scores = [student_course.score for student_course in student_courses]
#         grades = []
#         for score in scores:
#             grade = calculate_grades(score)
#             grades.append(grade)

#         total_grade_points = 0.0
#         total_credit_units = 0.0

#         for i in range(len(grades)):
#             if grades[i] == 'A':
#                 total_grade_points += 5 * credits[i]
#                 total_credit_units += credits[i]
#             elif grades[i] == 'B':
#                 total_grade_points += 4 * float(credits[i])
#                 total_credit_units += credits[i]
#             elif grades[i] == 'C':
#                 total_grade_points += 3 * credits[i]
#                 total_credit_units += credits[i]
#             elif grades[i] == 'D':
#                 total_grade_points += 2 * credits[i]
#                 total_credit_units += credits[i]
#             elif grades[i] == 'E':
#                 total_grade_points += 1 * credits[i]
#                 total_credit_units += credits[i]
#             elif grades[i] == 'F':
#                 total_grade_points += 0 * credits[i]
#                 total_credit_units += credits[i]
#         gpa = total_grade_points / total_credit_units
#         return {
#             'message': 'GPA calculated successfully',
#             'scores': scores,
#             'grades': grades,
#             'credits': credits,
#             'gpa': round(gpa, 2)
#         }

 
        



        




@grade_namespace.route('/student/courses/<int:course_id>')
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
#         credits = [student_course.course_unit for student_course in student_courses]
#         scores = [student_course.score for student_course in student_courses]
#         grades = []
#         for score in scores:
#             grade = calculate_grades(score)
#             grades.append(grade)

#         for i in range(len(scores)):
#             score = float(scores[i])

#             if score >= 70:
#                 grades.append('A')
#             elif score >= 60:
#                 grades.append('B')
#             elif score >= 50:
#                 grades.append('C')
#             elif score >= 45:
#                 grades.append('D')
#             elif score >= 40:
#                 grades.append('E')
#             else:
#                 grades.append('F')

#             course = {
#                 'course_code': student_courses[i].course_code,
#                 'course_unit': student_courses[i].course_unit,
#                 'score': scores[i],
#                 'grade': grades[i]
#             }


#         return course