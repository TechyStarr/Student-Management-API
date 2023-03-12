from flask_restx import Namespace ,fields



auth_namespace = Namespace('auth', description = 'name space for authentication')



user_model = auth_namespace.model(
    'Signup', {
		'name': fields.String(required=True, description="'User's Name"),
		'username': fields.String(required=True, description="User's Username"),
		'email': fields.String(required=True, description='User Email Address'),
        'user_type': fields.String(required=True, description='User Type'),	
		'password': fields.String(required=True, description='User Password')
	}
)

signup_model = auth_namespace.model(
    'Signup', {
		'name': fields.String(required=True, description="'User's Name"),
		'username': fields.String(required=True, description="User's Username"),
		'email': fields.String(required=True, description='User Email Address'),
        'user_type': fields.String(required=True, description='User Type'),	
	}
)



login_model = auth_namespace.model(
    'Login', {
		'email': fields.String(required=True, description='User email address'),
        'student_id': fields.String(required=True, description='User student id'),
		'password': fields.String(required=True, description='User Password')
	}
)






