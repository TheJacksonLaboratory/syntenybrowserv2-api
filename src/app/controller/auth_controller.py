"""
An example of how to provide basic (username,password) style auth
"""
from flask_restplus import Resource, Namespace, reqparse, fields
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_refresh_token_required, get_jwt_identity

# When implementing ldap, here are some example imports that might be useful
# from src.app.service.auth.jax_ldap import authenticate_user, InvalidCredentials, get_user_groups

NS = Namespace('auth')

TOKEN_MODEL = NS.model('tokens', {
    'refresh': fields.String(),
    'access': fields.String(),
})

TOKEN_FLOW_MODEL = NS.model('token_flow', {
    'auth_uri': fields.String(skip_none=True),
    'tokens': fields.Nested(TOKEN_MODEL, skip_none=True)
})


@NS.route('/login', methods=['POST'])
class UserLogin(Resource):
    """ Get access tokens """

    parser = reqparse.RequestParser()

    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    @NS.expect(parser, validate=True)
    @NS.marshal_with(TOKEN_MODEL)
    def post(self):
        """ Authenticate and create jwt """
        args = self.parser.parse_args()

        # Authenticate User TODO: Uncomment to use
        #
        # try:
        #     authenticate_user(args['username'], args['password'])
        # except InvalidCredentials as e:
        #     abort(401, message=str(e))

        identity = {
            'username': args['username'],
        }

        # Check User Role TODO: Uncomment to use
        #
        # if not identity['roles']['user'] and not identity['roles']['admin']:
        #     abort(401, "You are not authorized to use this functionality")

        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        return {
            'access': access_token,
            'refresh': refresh_token
        }


@NS.route('/refresh', methods=['POST'])
class UserRefresh(Resource):
    """ Get access token from refresh """

    @staticmethod
    @NS.doc(security='Refresh')
    @jwt_refresh_token_required
    def post():
        """ Create a new access token from a refresh token """

        identity = get_jwt_identity()

        return {
            'access': create_access_token(identity=identity)
        }
