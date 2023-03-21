from ..utils import db
from functools import wraps
from flask import request
from flask_restx import Resource, fields, Namespace, abort
from ..auth.views import generate_random_string
from ..models.user import Student
from ..models.courses import Course, StudentCourse
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity



admin_namespace = Namespace('Admin', description = 'Admin accessible route')

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # check if user is admin
        user_id = get_jwt_identity()
        if user_id == 'Student101':
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

retrieve_course_model = admin_namespace.model(
    'Course', {
        'id': fields.String(required=True),
        'course_code': fields.String(description="'Course Code"),
        'course_unit': fields.String(description="Course Unit"),
        'course_title': fields.String( description="Course Name"),
        'tutor_name': fields.String(required=True, description="Course Level")
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
		'student_id': fields.String(required=True, description="Studend ID")
	}
)

simple_student_model = admin_namespace.model(
    'SimpleStudent', {
        'id': fields.String(dump_only=True),
        'first_name': fields.String(required=True, description="Student's First Name"),
        'last_name': fields.String(required=True, description="'Student's Last Name"),
        'email': fields.String(required=True, description="Student's Email")
    }
)



student_course_model = admin_namespace.model(
    'StudentCourse', {
		'id': fields.String(required=True),
        'course_code': fields.String(description="'Course Code"),
        'course_unit': fields.Float( description="Course Name"),
        'score': fields.Float(required=True, default=0.0),
        'grade': fields.String(required=True, default='N/A'),
        'student_id': fields.String(required=True, description="Studend ID"),
	}
)







@admin_namespace.route('/students')
class GetStudents(Resource):
    
    @admin_namespace.marshal_with(simple_student_model, as_list=True)
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

        existing_email = Student.query.filter_by(email=data['email']).first()

        if existing_email:
            abort(409, message="This user already exists")


        new_student = Student(
            student_id='ALT00' + generate_random_string(3),
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        try:
            new_student.save()
            return new_student, HTTPStatus.CREATED, {
            'message': 'Student created successfully'
            }

        except Exception as e:
            return {
                'message': 'An error occured while creating student'
            }, HTTPStatus.BAD_REQUEST

        


@admin_namespace.route('/students/<int:student_id>')
class GetStudent(Resource):
    @admin_namespace.marshal_with(student_model)
    @admin_namespace.doc(
        description='Get a student',
    )
    @jwt_required()
    @is_admin
    def get(self, student_id):
        """
            Get a student by id
        """

        student = Student.query.filter_by(id=student_id).first()
        
        if not student:        
                    abort(404, message="Student does not exist")
        
        try:    
            return student, HTTPStatus.OK
        except Exception as e:
            return {
                'message': 'An error occured while retrieving student'
            }, HTTPStatus.BAD_REQUEST
        
    @admin_namespace.expect(simple_student_model)
    @admin_namespace.marshal_with(simple_student_model)
    @admin_namespace.doc(
        description='Update a student',
    )
    @jwt_required()
    @is_admin
    def patch(self, student_id):
        """
            Update a student by id
        """
        data = admin_namespace.payload
        update_student = Student.query.filter_by(id=student_id).first()

        if not update_student:
            abort(404, message="Student does not exist")

        update_student.first_name = data['first_name']
        update_student.last_name = data['last_name']
        update_student.email = data['email']

        try:
            update_student.update()
            return update_student, HTTPStatus.OK, {
            'message': 'Student updated successfully'
            }
        
        except Exception as e:
            return {
                'message': 'An error occured while updating student'
            }, HTTPStatus.BAD_REQUEST
        




    


# All endpoints for courses
@admin_namespace.route('/courses')
class GetCourses(Resource):
    
    @admin_namespace.marshal_with(retrieve_course_model, as_list=True)
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
        
        if not courses:        
                    abort(404, message="No course has been registered")
        try:
            return courses, HTTPStatus.OK
        except Exception as e:
            return {
                'message': 'An error occured while retrieving courses'
            }, HTTPStatus.BAD_REQUEST
    

    @admin_namespace.expect(create_course_model)
    @admin_namespace.marshal_with(show_course_model)
    @admin_namespace.doc(
        description="Create a new course"
    )
    @jwt_required()
    @is_admin
    def post(Self):
        """
            Create a new course, course_code and course_title must be unique
        """

        data = admin_namespace.payload

        course_code = Course.query.filter_by(course_code=data['course_code']).first()
        course_title = Course.query.filter_by(course_title=data['course_title']).first()

        if course_code or course_title:
            abort(409, message="This course already exists")

        new_course = Course(
            course_title = data['course_title'],
            course_code = data['course_code'],
            course_unit = data['course_unit'],
            tutor_name = data['tutor_name']
        )
        try:
            new_course.save()

            return new_course, HTTPStatus.CREATED, {
                'message': 'Course created successfully'
            }

        except Exception as e:
            return {
                'message': 'Something went wrong'
            }

    




    
@admin_namespace.route('/student/<int:student_id>/courses')
class GetStudentCourses(Resource):
    @admin_namespace.marshal_with(student_course_model)
    @admin_namespace.doc(
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
            abort(404, message="Student does not exist")

        student_course = StudentCourse.query.filter_by(student_id=student_id).all()
        if not student_course and student:
            abort(404, message="This student has not registered for any course")

        try:
            return student.registered_courses, HTTPStatus.OK
        except Exception as e:
            return {
                'message': 'An error occured while retrieving courses'
            }, HTTPStatus.BAD_REQUEST
        






    


@admin_namespace.route('/course/<int:course_id>')
class GetCourse(Resource):
    
    @admin_namespace.marshal_with(retrieve_course_model)
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
        course = Course.get_by_id(course_id)
        
        if course:
            try:
                return course, HTTPStatus.OK
            except Exception as e:
                return {
                    'message': 'An error occured while retrieving course'
                }, HTTPStatus.BAD_REQUEST   
        
        abort(404, message="This course does not exist")

        
    

    @admin_namespace.expect(retrieve_course_model)
    @admin_namespace.marshal_with(retrieve_course_model)
    @admin_namespace.doc(
        description='Update a course by id', params={
            'course_id': 'The course id'
        }
    )
    @jwt_required()
    @is_admin
    def patch(self, course_id):
        """
            Update course by id
        """

        update_course = Course.get_by_id(course_id)
        data = admin_namespace.payload

        update_course.course_title = data['course_title']
        update_course.course_code = data['course_code']
        update_course.course_unit = data['course_unit']
        update_course.score = data['score']
        update_course.tutor_name = data['tutor_name']

        if not update_course:
            abort(404, message="This course does not exist")

        try:
            update_course.update()

            return update_course, HTTPStatus.OK, {
                'message': 'Changes successfully made to {course.id}'
            }
        except Exception as e:
            return {
                'message': 'Something went wrong'
            }, HTTPStatus.BAD_REQUEST


    
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

        course = Course.query.filter_by(id=course_id).first()
        if not course:
            abort(404, message="This course does not exist")
        try:
            course.delete()
            return HTTPStatus.OK, {
                "message": "Course deleted successfully"
            }
        except Exception as e:
            return {
                'message': 'Something went wrong'
            }, HTTPStatus.BAD_REQUEST
    




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
        
        # current_user = get_jwt_identity()
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            abort(404, message="This student does not exist")

        course_code = admin_namespace.payload['course_code']
        course_code = StudentCourse.query.filter_by(course_code=course_code).first()
        if course_code and student.student_id:
            abort(409, message="This student has already registered for this course")
        
        data = admin_namespace.payload
        new_course = StudentCourse(
            course_code = data['course_code'],
            course_unit = data['course_unit'],
            score = data['score'],
            grade = data['grade'],
            student_id = student_id,
        )

        try:
            new_course.save()
            return new_course, HTTPStatus.CREATED, {
                'message': 'Student successfully registered for course'
            }
        except Exception as e:
            return {
                'message': 'Something went wrong'
            }, HTTPStatus.BAD_REQUEST


# All endpoints for the admin to handle grades




