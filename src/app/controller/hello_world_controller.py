"""
An example controller
"""
from flask_restplus import Resource, Namespace, reqparse
from celery.states import READY_STATES as CELERY_READY_STATES
from flask_jwt_extended import jwt_required
from .utils.jwt import required_jwt_matches_url, optional_jwt_matches_url

from ..service.hello_world_service import say_hello
from ..service.task_service_example import long_running_task


NS = Namespace('hello', description='The hello endpoint')


@NS.route('/sayhello')
class HelloWorld(Resource):
    """ Example unprotected routes """

    @staticmethod
    def get():
        """ Say hello """
        return say_hello(), 200


@NS.route('/pvt_hello')
class ProtectedHelloWorld(Resource):
    """ Examples protected routes """

    # Manually set endpoint to require authorization
    #  Use security=None to disable default required auth
    @staticmethod
    @NS.doc(security='Access')
    @jwt_required
    def get():
        """ Say hello if provided valid jwt """
        return say_hello(), 200


@NS.route('/pvt_hello_user/<int:user_id>')
class UserSpecificProtectedHelloWorld(Resource):
    """ Example that validates the user id in url matches provided token"""

    @staticmethod
    @NS.doc(security='Access')
    @required_jwt_matches_url('user_id', 'uid')
    def get(user_id):
        """ Say hello if valid jwt, and jwt contains user_id in url """
        return say_hello(user_id), 200


@NS.route('/pvt_hello_combined', '/pvt_hello_combined/<int:user_id>')
class UserOptionalProtectedHelloWorld(Resource):
    """ Example that validates the user id in url matches provided token"""

    @staticmethod
    @NS.doc(security=('Access', None))
    @optional_jwt_matches_url('user_id', 'uid')
    def get(user_id=None):
        """ Require JWT match url if JWT or URL id provided """
        return say_hello(user_id), 200


@NS.route('/slow_reverse')
class SlowReverser(Resource):
    """ Reverse a string using a task queue """

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('to_reverse', required=True)

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('task_id', required=True)

    @NS.expect(post_parser, validate=True)
    def post(self):
        """ Submit a string to reverse, returns task_id used to get result """
        args = self.post_parser.parse_args()
        res = long_running_task.apply_async([args['to_reverse']])
        result = {'id': res.task_id, 'input': args['to_reverse']}
        return result, 200

    @NS.expect(get_parser, validate=True)
    def get(self):
        """ Get the status, or status and result if ready """
        args = self.get_parser.parse_args()
        retval = long_running_task.AsyncResult(args['task_id'])
        response = {'status': retval.status}

        if retval.status in CELERY_READY_STATES:
            result = retval.get(timeout=1.0)
            response['result'] = repr(result)

        return response
