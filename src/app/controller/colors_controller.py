from flask_restplus import Resource, Namespace
# from flask_jwt_extended import jwt_required
from ..service.colors_service import get_colors

ns = Namespace('color-map', description='Returns mapping between chromosomes and their associated color coding colors.')


@ns.route('')
class ClientColors(Resource):

    @staticmethod
    def get():
        return get_colors(), 200
