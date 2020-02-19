import os
import json
import unittest
from repositories.task import TaskModel, TaskRepository

class UnitTestBase(unittest.TestCase):
    ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    def setUp(self):
        config_filepath = os.path.join(self.ROOT_PATH, 'config.test.json')

        with open(config_filepath, 'r') as fp:
            config = json.load(fp)

        os.environ['REGION'] = config['REGION']
        os.environ['AURORA_DB_HOST'] = config['AURORA_DB_HOST']
        os.environ['AURORA_DB_PORT'] = config['AURORA_DB_PORT']
        os.environ['AURORA_DB_NAME'] = config['AURORA_DB_NAME']
        os.environ['AURORA_DB_USER'] = config['AURORA_DB_USER']
        os.environ['AURORA_DB_PASSWORD'] = config['AURORA_DB_PASSWORD']
        repo = TaskRepository()

    def tearDown(self):
        repo = TaskRepository()
        sql = 'DROP DATABASE {}'.format(os.environ['AURORA_DB_NAME'])
        repo._execute(sql)

        del os.environ['REGION']
        del os.environ['AURORA_DB_HOST']
        del os.environ['AURORA_DB_PORT']
        del os.environ['AURORA_DB_NAME']
        del os.environ['AURORA_DB_USER']
        del os.environ['AURORA_DB_PASSWORD']
