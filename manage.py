"""
This is the manager entrypoint to the application
"""

import os
from flask_script import Manager
from flask_migrate import MigrateCommand

from src.app import create_app
from src.cli.run import RunCommand
from src.cli.test import RunTestsCommand, RunTestsXMLCommand
from src.cli.celery import StartCeleryWorkersCommand
from src.cli.config import GenerateSecretsCommand, InitConfigCommand

MANAGER = Manager(create_app(os.getenv('FLASK_CONFIG') or 'dev'))

# Run the application
MANAGER.add_command('run', RunCommand())

# Perform database operations
MANAGER.add_command('db', MigrateCommand)

# Manage the 'synbrowser.config' file
MANAGER.add_command('create_secrets', GenerateSecretsCommand)
MANAGER.add_command('init_config', InitConfigCommand)


# Start and stop celery workers
MANAGER.add_command('start_workers', StartCeleryWorkersCommand())

# Run test
MANAGER.add_command('test', RunTestsCommand())
MANAGER.add_command('test_xml', RunTestsXMLCommand())


if __name__ == '__main__':
    MANAGER.run()
