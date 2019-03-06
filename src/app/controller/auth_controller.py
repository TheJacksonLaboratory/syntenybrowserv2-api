from flask_restplus import abort, Resource, Namespace, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity

from src.app.service.auth.jax_ldap import authenticate_user, InvalidCredentials, get_user_groups

ns = Namespace('auth')


def _get_user_roles(username):
    # groups = get_user_groups(username)

    # TODO: Implement user role rules
    return {
        'admin': False,
        'user': True
    }


@ns.route('/login', methods=['POST'])
class UserLogin(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    @ns.expect(parser, validate=True)
    def post(self):
        args = self.parser.parse_args()

        # Authenticate User TODO: Uncomment to use
        '''
        try:
            authenticate_user(args['username'], args['password'])
        except InvalidCredentials as e:
            abort(401, message=str(e))
        '''

        identity = {
            'username': args['username'],
            'roles': _get_user_roles(args['username'])
        }

        # Check User Role TODO: Uncomment to use
        '''
        if not identity['roles']['user'] and not identity['roles']['admin']:
            abort(401, "You are not authorized to use this functionality")
        '''
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=args['username'])

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }


@ns.route('/refresh', methods=['POST'])
class UserRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        username = get_jwt_identity()

        identity = {
            'username': username,
            'roles': _get_user_roles(username)
        }

        return {
            'access_token': create_access_token(identity=identity)
        }
