from flask_restplus import Resource, Namespace
# from flask_jwt_extended import jwt_required
from ..service.colors_service import get_colors

ns = Namespace('colors', description='Endpoint to return color scheme to be used in genome color coding.')


@ns.route('')
class ClientColors(Resource):

    @staticmethod
    def get():
        return get_colors(), 200
