from ..utils import db
from flask import request
from flask_restx import Resource, fields, Namespace, abort
from ..admin.views import student_model
from ..models.user import Student
from ..models.courses import StudentCourse
from ..admin.grades import  calculate_grades
from http import HTTPStatus
from flask_jwt_extended import jwt_required


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
    @student_namespace.expect(student_model)
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
        student = Student.query.filter_by(id=student_id).first()

        if student is None:
            abort (404, message="Student not found")
        
    
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.email = data['email']
        # student.password = data['password']
        try:
            student.update()

            return student, HTTPStatus.OK, {
                'message': 'Your profile has been updated successfully'
            }
        except Exception as e:
            return {
                'message': 'Something went wrong'
            }, HTTPStatus.BAD_REQUEST




    
@student_namespace.route('/student/<int:student_id>/scores')
class StudentScore(Resource):
    # @grade_namespace.marshal_with(student_score_model)
    @student_namespace.doc(
        description='Get all scores', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Get all scores
        """
        
        student_courses = StudentCourse.query.filter_by(student_id=student_id).all()
        if not student_courses:
            return {
                'message': "This student wasn't registered for any course"
            }, HTTPStatus.BAD_REQUEST
        student_id = [student_course.student_id for student_course in student_courses]
        course_code = [student_course.course_code for student_course in student_courses]
        credits = [student_course.course_unit for student_course in student_courses]
        scores = [student_course.score for student_course in student_courses]
        grades = []
        for score in scores:
            grade = calculate_grades(score)
            grades.append(grade)

        courses = []

        for i in range(len(scores)):
            score = scores[i]

            if score >= 70:
                grades =  'A'  
            elif score >= 60:
                grades =  'B'  
            elif score >= 50:
                grades =  'C'  
            elif score >= 45:
                grades =  'D'  
            elif score >= 40:
                grades =  'E'  
            else:
                grades =  'F'  

            course = {
                'student_id': student_id[i],
                'course_code': course_code[i],
                'credits': credits[i],
                'score': scores[i],
                'grade': grades[:1]
            }

            courses.append(course)


        return courses, HTTPStatus.OK
    