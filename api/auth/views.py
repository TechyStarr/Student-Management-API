import uuid
import random
import string
from ..utils import db
from ..mails.mails import send_mail
from flask import request
from flask_restx import Resource
from .serializers import login_model, signup_model
from ..models.user import User, Student, Admin, Tutor
from .serializers import auth_namespace
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies




# concatenate id with strings to form unique id
# record = Student.query.get(id)

# random_string = str(uuid.uuid4())

# student_id = str(record.id) + "-ALT00" + str(record.id)


def generate_random_string(self):
	"""
		Generate random string of specified length
	"""

	characters = string.ascii_letters + string.digits
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
			return {
				'message': 'User already exists'
			}, HTTPStatus.BAD_REQUEST
		
		# email = email
		# student_id = student_id
		password = generate_password(self)


		if data.get('user_type') == 'admin':
			nomination = 'Admin'
			new_user = Admin(
				name = data.get('name'),
				username = data.get('username'),
				email = data.get('email'),
				password = generate_password(self),
				nomination = nomination,
				user_type = data.get('user_type'),
				is_admin = True
			)

		
		elif data.get('user_type') == 'student':
			admission_no = 'ALT' +  generate_random_string(3)
			new_user = Student(
				name = data.get('name'),
				username = data.get('username'),
				email = data.get('email'),
				matric_no = admission_no,
				password = generate_password(self),
				user_type = data.get('user_type')
			)


		elif data.get('user_type') == 'tutor':
			staff = 'TUT' +  generate_random_string(3)
			new_user = Tutor(
				name = data.get('name'),
				username = data.get('username'),
				email = data.get('email'),
				tutor_no = staff,
				user_type = data.get('user_type')
			)



		else:
			return {
				'message': 'Invalid user type'
			}, HTTPStatus.BAD_REQUEST
		
		try:
			new_user.save()
			send_mail(new_user, password)
			return {
				'message': f'User {new_user.name} created successfully as {new_user.user_type}'
			}
		except:
			db.session.rollback()
			return {
				'message': 'An error occurred while creating user'
			}, HTTPStatus.INTERNAL_SERVER_ERROR
		


		


@auth_namespace.route('/login')
class Login(Resource):
	@auth_namespace.expect(login_model)
	def post(self):
		"""
			Generate JWT Token
		"""

		data = request.get_json()
		
		email = data.get('email')
		password = data.get('password')

		user = User.query.filter_by(email=email).first()

		if (user is not None) and check_password_hash(user.password_hash, password):
			access_token = create_access_token(identity=user.username)
			refresh_token = create_refresh_token(identity=user.username)

			response = {
				'access_token': access_token,
				'refresh_token': refresh_token
			}

			return response, HTTPStatus.CREATED


@auth_namespace.route('/refresh')
class Refresh(Resource):
	@jwt_required(refresh=True)
	def post(self):
		"""
			Generate refresh Token
		"""

		username = get_jwt_identity()

		access_token = create_access_token(identity=username)

		return {'access_token': access_token}, HTTPStatus.OK


@auth_namespace.route('/logout')
class Logout(Resource):
	@jwt_required
	def post(self):
		"""
		Log the user out
		"""
		unset_jwt_cookies
		db.session.commit()
		return {"message": "Successfully Logged Out"}, HTTPStatus.OK
