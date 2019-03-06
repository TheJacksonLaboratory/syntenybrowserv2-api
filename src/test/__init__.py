from flask_testing import TestCase
from src.application import app
from src.config import config_by_name
from src.app.model import init_db, Session, drop_all


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(config_by_name['test'])
        self.engine = init_db(app)
        self.session = Session
        self.query = self.session.query
        return app


class BaseDBTestCase(BaseTestCase):
    def setup(self):
        pass

    def tearDown(self):
        self.session.remove()
        drop_all(self.engine)

