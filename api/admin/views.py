import uuid
import random
import string
from ..utils import db
from flask import request
from flask_restx import Resource, fields, Namespace
from ..auth.views import generate_random_string, generate_password
from ..models.user import Student, User, Tutor
from ..models.courses import Course, StudentCourse
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from redis import Redis


admin_namespace = Namespace('student', description = 'Admin accessible route')





course_model = admin_namespace.model(
    'Course', {
        'id': fields.String(required=True),
        'course_title': fields.String(required=True, description="Course Name"),
        'course_code': fields.String(required=True, description="'Course Code"),
        'course_description': fields.String(required=True, description="Course Description"),
        'course_unit': fields.String(required=True, description="Course Unit"),
        'course_level': fields.String(required=True, description="Course Level"),
        'score': fields.Float(required=True, default=0.0),
        'tutor_name': fields.String(required=True, description="Course Level"),
        
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
        'courses': fields.String(required=True, description='courses for a student' ),
		'gpa': fields.String( required=True, description='Student gpa')
        
	}
)





student_course_model = admin_namespace.model(
    'StudentCourse', {
        'id': fields.String(required=True, description="'User's Name"),
        'course_id': fields.String(required=True, description="Student's First Name"),
        'student_id': fields.String(required=True, description="'Student's Last Name"),
        'grade': fields.String(required=True, description="Studend ID")
    }
)




# Retrieve the student from the database using student_id/matric no
# Use the student's login details to autheticate the request
# Create a new course oject with the given data
# Add the course to the student's courses list
# Save the changes to the database



@admin_namespace.route('/students')
class GetStudents(Resource):
    
    @admin_namespace.marshal_with(student_model, as_list=True)
    @admin_namespace.doc(
        description='Get all registered students',
    )
    @jwt_required()
    def get(self):
        """
            Retrieve all students
        """

        students = Student.query.all()
        
        if students is None:        
                    return {
                        'message': 'No student has been registered'
                    }, HTTPStatus.BAD_REQUEST
        
        return students, HTTPStatus.OK
    

    @admin_namespace.expect(student_model)
    @admin_namespace.marshal_with(student_model)
    @admin_namespace.doc(
        description="Create a new student"
    )
    @jwt_required()
    def post(Self):
        """
            Create a new student
        """
            
        # username = get_jwt_identity()
        # current_user = User.query.filter_by(username=username).first()
        data = admin_namespace.payload

        student = Student.query.filter_by(student_id=data['student_id']).first()

        if student:
            return {
                'message': 'This student already exists'
            }, HTTPStatus.BAD_REQUEST

        new_student = Student(
            student_id = 'ALT00' + generate_random_string(1),
            email = data['email'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            password_hash = data['password'],
            # registered_courses=['registered_courses'],
            gpa=data['gpa']
        )

        new_student.save()

        return new_student, HTTPStatus.CREATED, {
            'message': 'Student created successfully'
        }
    


@admin_namespace.route('/student/<int:student_id>')
class GetUpdateDelete(Resource):

    @admin_namespace.marshal_with(student_model)
    @admin_namespace.doc(
        description='Get a student by id', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
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
        description='Update a student by id', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
    def put(self, student_id):
        """
            Update a student by id
        """

        update_student = Student.get_by_id(student_id)
        data = admin_namespace.payload

        update_student.first_name = data['first_name']
        update_student.last_name = data['last_name']
        update_student.password = data['password']
        # update_student.registered_courses = data['registered_courses']
        # update_student.gpa = data['gpa']

        update_student.update()

        return update_student, HTTPStatus.OK, {
            'message': 'Student updated successfully'
        }
    

    @admin_namespace.expect(student_model)
    @admin_namespace.marshal_with(student_model)
    @admin_namespace.doc(
        description='Delete a student by id', params={
            'student_id': 'The student id'
        }  
    )
    @jwt_required()
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
    
    @admin_namespace.marshal_with(course_model, as_list=True)
    @admin_namespace.doc(
        description='Get all registered courses',
    )
    @jwt_required()
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
    

    @admin_namespace.expect(course_model)
    @admin_namespace.marshal_with(course_model)
    @admin_namespace.doc(
        description="Create a new course"
    )
    @jwt_required()
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
            course_description = data['course_description'],
            course_unit = data['course_unit'],
            course_level = data['course_level'],
            score = data['score'],
            tutor_name = data['tutor_name']
        )

        new_course.save()

        return new_course, HTTPStatus.CREATED, {
            'message': 'Course created successfully'
        }
    


@admin_namespace.route('/course/<int:course_id>')
class GetUpdateDelete(Resource):
    
    @admin_namespace.marshal_with(course_model)
    @admin_namespace.doc(
        description='Get a course by id', params={
            'course_id': 'The course id'
        }
    )
    @jwt_required()
    def get(self, course_id):
        """
            Retrieve a course by id
        """

        course = Course.get_by_id(course_id)
        
        if course is None:  
                    return {
                        'message': 'This student does not exist'
                    }, HTTPStatus.BAD_REQUEST

        return course, HTTPStatus.OK
    

    @admin_namespace.expect(course_model)
    @admin_namespace.marshal_with(course_model)
    @admin_namespace.doc(
        description='Update a course by id', params={
            'course_id': 'The course id'
        }
    )
    @jwt_required()
    def patch(self, course_id):
        """
            Update a course by id
        """
        current_user = get_jwt_identity()

        update_course = Course.get_by_id(course_id)
        data = admin_namespace.payload

        update_course.course_title = data['course_title']
        update_course.course_code = data['course_code']
        update_course.course_description = data['course_description']
        update_course.course_unit = data['course_unit']
        update_course.score = data['score']
        update_course.tutor_name = data['tutor_name']
        # update_student.registered_courses = data['registered_courses']
        # update_student.gpa = data['gpa']

        update_course.update()

        return update_course, HTTPStatus.OK, {
            'message': 'Changes successfully made to {course.id}'
        }
    

    @admin_namespace.expect(course_model)
    @admin_namespace.marshal_with(course_model)
    @admin_namespace.doc(
        description='Delete a course by id', params={
            'course_id': 'The course id'
        }  
    )
    @jwt_required()
    def delete(self, course_id):
        """
            Delete a course by id
        """

        course = Course.get_by_id(course_id)

        course.delete()

        return HTTPStatus.OK, {
            "message": "Course deleted successfully"
        }
    








@admin_namespace.route('/courses/<int:course_id>/register/<int:student_id>')
class RegisterStudentCourse(Resource):
    
    @admin_namespace.expect(course_model)
    # @admin_namespace.marshal_with(student_course_model)
    @admin_namespace.doc(
        description='Register a student for a course', params={
            'student_id': 'The student id',
            'course_id': 'The course id'
        }
    )
    @jwt_required()
    def post(self, student_id, course_id):
        """
            Register a student for a course using student_id and course_id
        """
        
        current_user_id = get_jwt_identity() 

        student = Student.query.filter_by(id=current_user_id).first()   
        data = request.get_json()
        course = Course.query.filter_by(id=data.get('course_id')).first()  
        if course:
            #check if student is already registered for this course
            get_student_in_course = StudentCourse.query.filter_by(student_id=student.id, course_id=course.id).first()
            if get_student_in_course:
                return {
                    'message':'Course has already been registered'
                    } , HTTPStatus.OK
            # Register the student to the course
            add_student_to_course = StudentCourse(student_id=student.id, course_id=course.id)
            try:
                add_student_to_course.save()
                return {'message': 'Course registered successfully'} , HTTPStatus.CREATED
            except:
                db.session.rollback()
                return {'message': 'An error occurred while registering course'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'Course does not exist'} , HTTPStatus.NOT_FOUND
    
    












# All endpoints for the admin to handle grades


@admin_namespace.route('/student/<int:student_id>/course/<int:course_id>')
class CalculateGPA(Resource):
    
    @admin_namespace.marshal_with(student_model)
    @admin_namespace.doc(
        description='Calculate a student GPA', params={
            'student_id': 'The student id'
        }
    )
    @jwt_required()
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
            for course in student.registered_courses:
                gpa += course.grade
            gpa = gpa / len(student.registered_courses)
            student.gpa = gpa
            student.update()
            


            return student, HTTPStatus.OK
        


        



