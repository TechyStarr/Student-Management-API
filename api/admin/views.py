import uuid
import random
import string
from ..utils import db
from functools import wraps
from flask import request, abort
from flask_restx import Resource, fields, Namespace
from ..auth.views import generate_random_string, generate_password
from ..models.user import Student, User
from ..models.courses import Course, StudentCourse
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies



admin_namespace = Namespace('Admin', description = 'Admin accessible route')

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


create_course_model = admin_namespace.model(
    'Course', {
        'id': fields.String(required=True),
        'course_code': fields.String(description="'Course Code"),
        'course_unit': fields.String(description="Course Unit"),
        'course_title': fields.String( description="Course Name"),
        'tutor_name': fields.String(required=True, description="Course Level"),
        'score': fields.Float(required=True, default=0.0),
        'grade': fields.String(required=True, default='N/A')
    }
)




course_list_model = admin_namespace.model(
    'CourseList', {
        'courses': fields.List(fields.Nested(create_course_model))
    }
)



show_course_model = admin_namespace.model(
    'ShowCourse', {
        'id': fields.String(required=True),
        'course_title': fields.String(required=True, description="Course Name"),
        'course_code': fields.String(required=True, description="'Course Code"),
        'course_unit': fields.String(required=True, description="Course Unit"),
        'score': fields.Float(required=True, default=0.0),
        'tutor_name': fields.String(required=True, description="Course Level")
    }
)



student_model = admin_namespace.model(
    'Student', {
		'id': fields.String(required=True),
        'first_name': fields.String(required=True, description="Student's First Name"),
        'last_name': fields.String(required=True, description="'Student's Last Name"),
        'email': fields.String(required=True, description="Student's Email"),
		'student_id': fields.String(required=True, description="Studend ID"),
		'password': fields.String(required=True, default="Student101", description="Student's Password"),
        'registered_courses': fields.List(fields.Nested(course_list_model)),
		'gpa': fields.String( required=True, description='Student gpa')
        
	}
)

simple_student_model = admin_namespace.model(
    'SimpleStudent', {
        'id': fields.String(dump_only=True),
        'first_name': fields.String(required=True, description="Student's First Name"),
        'last_name': fields.String(required=True, description="'Student's Last Name"),
        'email': fields.String(required=True, description="Student's Email"),
        'password': fields.String(required=True, default="Student101", description="Student's Password"),
    }
)



student_course_model = admin_namespace.model(
    'StudentCourse', {
		'id': fields.String(required=True),
        'course_code': fields.String(description="'Course Code"),
        'course_unit': fields.String( description="Course Name"),
        'score': fields.Float(required=True, default=0.0),
        'grade': fields.String(required=True, default='N/A'),
        'first_name': fields.String(required=True, description="Student's First Name"),
        'last_name': fields.String(required=True, description="'Student's Last Name"),
        'student_id': fields.String(required=True, description="Studend ID"),
        'course_id': fields.String(required=True, description="Course ID"),


	}
)




score_model = admin_namespace.model(
    'Score', {
        'id': fields.String(required=True, description="'User's Name"),
        'student_id': fields.String(required=True, description="'Student's Last Name"),
        'course_id': fields.String(required=True, description="Student's First Name"),
        'score': fields.Float(required=True, description="Student's First Name"),
    }
)






@admin_namespace.route('/students')
class GetStudents(Resource):
    
    @admin_namespace.marshal_with(student_model, as_list=True)
    @admin_namespace.doc(
        description='Get all students',
    )
    @jwt_required()
    @is_admin
    def get(self):
        """
            Get all students
        """

        students = Student.query.all()
        
        if students is None:        
                    return {
                        'message': 'No student has been registered'
                    }, HTTPStatus.BAD_REQUEST
        
        return students, HTTPStatus.OK
    

    @admin_namespace.expect(simple_student_model)
    @admin_namespace.marshal_with(simple_student_model)
    @admin_namespace.doc(description="Create a new student")
    @jwt_required()
    @is_admin
    def post(self):
        """
        Create a new student
        """
        data = admin_namespace.payload

        # student = Student.query.filter_by(student_id=data['student_id']).first()
        existing_email = Student.query.filter_by(email=data['email']).first()

        if existing_email:
            return {
                'message': 'This email already exists'
            }, HTTPStatus.BAD_REQUEST


        new_student = Student(
            student_id='ALT00' + generate_random_string(1),
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        new_student.save()

        

        return new_student, HTTPStatus.CREATED, {
            'message': 'Student created successfully'
        }



@admin_namespace.route('/student/<int:student_id>')
class GetUpdateDeleteStudent(Resource):

    @admin_namespace.marshal_with(student_model)
    @admin_namespace.doc(
        description='Get a student by id', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    @is_admin
    def get(self, student_id):
        """
            Retrieve a student by id
        """

        student = Student.get_by_id(student_id)
        
        if student is None:  
                    return {
                        'message': 'This student does not exist'
                    }, HTTPStatus.BAD_REQUEST

        return student, HTTPStatus.OK
    


    

    @admin_namespace.expect(student_model)
    @admin_namespace.marshal_with(student_model)
    @admin_namespace.doc(
        description='Delete a student by id', params={
            'student_id': 'The student id'
        }  
    )
    @jwt_required()
    @is_admin
    def delete(self, student_id):
        """
            Delete a student by id
        """

        student = Student.get_by_id(student_id)

        student.delete()

        return HTTPStatus.OK, {
            "message": "Student deleted successfully"
        }
    


# All endpoints for courses
@admin_namespace.route('/courses')
class GetCourses(Resource):
    
    @admin_namespace.marshal_with(create_course_model, as_list=True)
    @admin_namespace.doc(
        description='Get all registered courses',
    )
    @jwt_required()
    @is_admin
    def get(self):
        """
            Retrieve all courses
        """

        courses = Course.query.all()
        
        if courses is None:        
                    return {
                        'message': 'No student has been registered'
                    }, HTTPStatus.BAD_REQUEST
        
        return courses, HTTPStatus.OK
    

    @admin_namespace.expect(create_course_model)
    @admin_namespace.marshal_with(create_course_model)
    @admin_namespace.doc(
        description="Create a new course"
    )
    @jwt_required()
    @is_admin
    def post(Self):
        """
            Create a new course
        """
            
        # username = get_jwt_identity()
        # current_user = User.query.filter_by(username=username).first()
        data = admin_namespace.payload

        course = Course.query.filter_by(id=data['id']).first()

        if course:
            return {
                'message': 'This Course already exists'
            }, HTTPStatus.BAD_REQUEST

        new_course = Course(
            course_title = data['course_title'],
            course_code = data['course_code'],
            course_unit = data['course_unit'],
            tutor_name = data['tutor_name']
        )

        new_course.save()

        return new_course, HTTPStatus.CREATED, {
            'message': 'Course created successfully'
        }
    



@admin_namespace.route('/course/<int:course_id>/students')
class GetStudentsForCourse(Resource):
    # @admin_namespace.marshal_with(student_model)
    @admin_namespace.doc(
        description='Retrieve all students for a particular course', params={
            'course_id': 'The course id'
        }
    )
    @jwt_required()
    @is_admin
    def get(self, course_id):
        """
            Retrieve all students for a particular course
        """
        courses = StudentCourse.query.filter_by(id=course_id).all()
        for course in courses:
            students = Student.query.all()
            if students not in courses:
                return students, HTTPStatus.OK
            return {
                'message': 'No student has been registered for this course'
            }
        return {
            'message': 'Course does not exist'
        }





    


@admin_namespace.route('/course/<int:course_id>')
class GetCourse(Resource):
    
    @admin_namespace.marshal_with(create_course_model)
    @admin_namespace.doc(
        description='Get a course by id', params={
            'course_id': 'The course id',
        }
    )
    @jwt_required()
    @is_admin
    def get(self, course_id):
        """
            Retrieve a course by id
        """
        data = request.get_json()
        course = Course.get_by_id(course_id)
        
        if course is None:  
                    return {
                        'message': 'This course does not exist'
                    }, HTTPStatus.BAD_REQUEST

        return course, HTTPStatus.OK
    

    @admin_namespace.expect(create_course_model)
    @admin_namespace.marshal_with(create_course_model)
    @admin_namespace.doc(
        description='Update a course by id', params={
            'course_id': 'The course id'
        }
    )
    @jwt_required()
    @is_admin
    def patch(self, course_id, student_id):
        """
            Update course by id
        """

        update_course = Course.get_by_id(course_id)
        data = admin_namespace.payload

        update_course.course_title = data['course_title']
        update_course.course_code = data['course_code']
        update_course.course_description = data['course_description']
        update_course.course_unit = data['course_unit']
        update_course.score = data['score']
        update_course.tutor_name = data['tutor_name']
        update_course.grade = data['grade']

        update_course.update()

        return update_course, HTTPStatus.OK, {
            'message': 'Changes successfully made to {course.id}'
        }


        
    @admin_namespace.doc(
        description='Delete a course by id', params={
            'course_id': 'The course id'
        }  
    )
    @jwt_required()
    @is_admin
    def delete(self, course_id):
        """
            Delete a course by id
        """

        course = Course.get_by_id(course_id)
        if course is None:
            return {
                'message': 'This course does not exist'
            }, HTTPStatus.BAD_REQUEST

        course.delete()

        return HTTPStatus.OK, {
            "message": "Course deleted successfully"
        }
    








@admin_namespace.route('/student/<int:student_id>')
class RegisterStudentCourse(Resource):
    
    @admin_namespace.expect(student_course_model)
    @admin_namespace.marshal_with(student_course_model)
    @admin_namespace.doc(
        description='Register a student for a course'
    )
    @jwt_required()
    @is_admin
    def post(self, student_id):
        """
            Register a student for a course using student_id and course_id
        """
        
        current_user = get_jwt_identity()
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {
                'message': 'This student does not exist'
            }, HTTPStatus.BAD_REQUEST
        
        data = admin_namespace.payload
        new_course = StudentCourse(
            course_code = data['course_code'],
            course_unit = data['course_unit'],
            score = data['score'],
            grade = data['grade'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            student_id = student_id,
            course_id = data['course_id']
        )
        new_course.save()

        return new_course, HTTPStatus.CREATED, {
            'message': 'Student successfully registered for course'
        }

        
    









# All endpoints for the admin to handle grades




