from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        'first_name': fields.String(required=True, description='user firstname'),
        'last_name': fields.String(required=True, description='user firstname'),
        'address1' : fields.String(required=True, description='user unit number and complext name'),
        'address2' : fields.String(required=True, description='user street number and street name')
        #'country': fields.String(required=True, description='user home country')
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })