import os
import json
import uuid
import unittest
import datetime
from tests.unit.test_base import UnitTestBase
from repositories.task import TaskModel, TaskRepository
from task_manager import task_manager

class TestTaskManager(UnitTestBase):
    def test_task_manager_add_task(self):
        task_id = uuid.uuid4()
        message = {
            'method': 'ADD',
            'body': {
                'task_id': str(task_id),
                'scheduled': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'task_type': 'send_gmail',
                'invoke_method': 'REST',
                'call_arn_url': 'https://serverless.com',
                'parameters': {},
                'data': {}
            }
        }
        event = {'Records':[{'Sns':{'Message': json.dumps(message)}}]}

        passed = True
        try:
            task_manager(event, {})
        except:
            passed = False

        self.assertTrue(passed, 'Add task through SNS failed.')

    def test_task_manager_update_task(self):
        task_id = uuid.uuid4()
        scheduled = datetime.datetime.utcnow()
        new_task = TaskModel(task_id, scheduled)
        repo = TaskRepository()
        created_task = repo.add_task(new_task)

        created_task.call_arn_url='https://google.com'
        message = {
            'method': 'UPDATE',
            'body': created_task.__dict__
        }
        event = {'Records':[{'Sns':{'Message': json.dumps(message)}}]}

        passed = True
        try:
            task_manager(event, {})
        except:
            passed = False

        self.assertTrue(passed, 'Update task through SNS failed.')

    def test_task_manager_delete_task(self):
        task_id = uuid.uuid4()
        scheduled = datetime.datetime.utcnow()
        new_task = TaskModel(task_id, scheduled)

        repo = TaskRepository()
        created_task = repo.add_task(new_task)

        message = {
            'method': 'DELETE',
            'body': {'id': created_task.task_id}
        }
        event = {'Records':[{'Sns':{'Message': json.dumps(message)}}]}

        passed = True
        try:
            task_manager(event, {})
        except:
            passed = False

        self.assertTrue(passed, 'Delete task through SNS failed.')

if __name__ == '__main__':
    unittest.main()