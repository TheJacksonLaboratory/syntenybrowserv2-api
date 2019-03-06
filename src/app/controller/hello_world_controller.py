from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from ..service.hello_world_service import say_hello


ns = Namespace('hello', description='The hello endpoint')


@ns.route('/sayhello')
class HelloWorld(Resource):

    @staticmethod
    def get():
        return say_hello(), 200

@ns.route('/protectedhello')
class ProtectedHelloWorld(Resource):

    # Manually set endpoint to require authorization
    #  Use security=None to disable default required auth
    @ns.doc(security='Bearer Auth')
    @jwt_required
    def get(self):
        return say_hello(), 200
