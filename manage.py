import sys
import unittest
import logging

from flask_script import Manager

from flask_migrate import Migrate, MigrateCommand

from src.app.model.hello_world_model import Hello


from src.application import app
from src.app.model import Base

manager = Manager(app)


migrate = Migrate(app, Base)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    logging.basicConfig(stream=sys.stderr)
    tests = unittest.TestLoader().discover('src/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
