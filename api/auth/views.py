import uuid
import random
import string
from ..utils import db
from ..utils.blocklist import BLOCKLIST
from flask import request
from flask_restx import Resource, fields, Namespace, abort
from ..models.user import User
from ..models.user import Student
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError



auth_namespace = Namespace('auth', description='Authentication Endpoints')



signup_model = auth_namespace.model(
    'Signup', {
		'username': fields.String(required=True, description="User's Username"),
		'email': fields.String(required=True, description='User Email Address'),
		'password_hash': fields.String(required=True, description='User Password')
	}
)




login_model = auth_namespace.model(
    'Login', {
		'email': fields.String(required=True, description='User email address'),
		'password': fields.String(required=True, description='User Password')
	}
)





def generate_random_string(self):
	"""
		Generate random string of specified length
	"""

	characters =  string.digits
	random_string = ''.join(random.choice(characters) for i in range(3))

	return random_string




def generate_password(self):
	"""
		Generate password of specified length with random strings
	"""

	characters = string.ascii_letters + string.digits
	password = ''.join(random.choice(characters) for i in range(10))

	return password







@auth_namespace.route('/signup')
class SignUp(Resource):
	@auth_namespace.expect(signup_model)
	@auth_namespace.marshal_with(signup_model)
	def post(self):
		"""
			Register a user
		"""
		data = request.get_json()

		# check if user already exists
		user = User.query.filter_by(email=data.get('email')).first()
		if user:
			abort(409, message=f'User {user.username} already exists')
		
		# email = email
		# student_id = student_id
		# password = generate_password(self)


		new_user = User(
			username = data.get('username'),
			email = data.get('email'),
			password_hash = generate_password_hash(data.get('password_hash')),
			is_admin = True
		)
		try:
			new_user.save()
			return new_user, HTTPStatus.CREATED, {
				'message': f'User {new_user.username} created successfully'
			}
		except Exception as e:
			db.session.rollback()
			return {
				'message': 'Something went wrong'
			}, HTTPStatus.INTERNAL_SERVER_ERROR



@auth_namespace.route('/login')
class StudentLogin(Resource):

	@auth_namespace.expect(login_model)
	def post(self):
		"""
			Generate JWT Token for both admin and student
		"""
		data = request.get_json()

		email = data.get('email')
		password = data.get('password')

		user = User.query.filter_by(email=email).first()
		
		if (user is not None) and email and check_password_hash(user.password_hash, password): 
			access_token = create_access_token(identity=user.username)
			refresh_token = create_refresh_token(identity=user.username)

			response = {
				'message': 'Logged in as {}'.format(user.username),
				'access_token': access_token,
				'refresh_token': refresh_token
			}
			return response, HTTPStatus.ACCEPTED

		if not user:
		
			student = Student.query.filter_by(email=email).first()
			if (student is not None) and check_password_hash(student.password_hash, password):
				access_token = create_access_token(identity=student.email)
				refresh_token = create_refresh_token(identity=student.email)
				

				response = {
					'message': 'Logged in as {}'.format(student.student_id),
					'access_token': access_token,
					'refresh_token': refresh_token
				}
				abort(200, message=response)

			abort(401, message='Invalid Credentials')



@auth_namespace.route('/refresh')
class Refresh(Resource):
	@jwt_required(refresh=True)
	def post(self):
		"""
			Refresh JWT access Token
		"""

		identity = get_jwt_identity()

		access_token = create_access_token(identity=identity)

		response = {
			'message': 'Access Token Refreshed',
			'access_token': access_token
		}
		return response, HTTPStatus.OK


@auth_namespace.route('/logout')
class Logout(Resource):
	@jwt_required
	def post(self):
		"""
			Log the user out
		"""
		token = get_jwt()
		jti = token['jti']
		token_type = token['type']
		BLOCKLIST.add(jti)

		response = {
			'message': 'Successfully Logged Out, Token revoked'
		}
		try:
			return response, HTTPStatus.OK
		except Exception as e:
			return {
				'message': 'Something went wrong'
			}, HTTPStatus.INTERNAL_SERVER_ERROR
		

# @auth_namespace.route('/reset-password')
# class ResetPassword(Resource):
# 	@jwt_required
# 	def post(self):
# 		"""
# 			Reset password
# 		"""
# 		data = request.get_json()


# 		email = data.get('email')
# 		password = data.get('password')
# 		confirm_password = data.get('confirm_password')

# 		user = User.query.filter_by(email=email).first()

# 		if user:
# 			user.password_hash = generate_password_hash(password)
# 			user.save()
# 			return {
# 				'message': 'Password reset successful'
# 			}, HTTPStatus.OK

# 		else:
# 			return {
# 				'message': 'User does not exist'
# 			}, HTTPStatus.NOT_FOUND
