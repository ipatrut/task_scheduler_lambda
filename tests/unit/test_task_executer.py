import os
import uuid
import unittest
import datetime
from tests.unit.test_base import UnitTestBase
from repositories.task import TaskModel, TaskRepository
from task_executer import task_executer
from botocore.exceptions import ClientError


class TestTaskExecuter(UnitTestBase):
    def test_rest_task_executer(self):
        task_id = uuid.uuid4()
        task = TaskModel(
            task_id,
            scheduled=datetime.datetime.now(),
            task_type='send_gmail',
            invoke_method='REST',
            call_arn_url='https://serverless.com',
            data={},
        )
        repo = TaskRepository()
        repo.add_task(task)

        passed = True
        try:
            task_executer(event={}, context={})
        except:
            passed = False

        self.assertTrue(passed, 'Execute REST task with CloudWatch failed.')

    def test_sns_task_executer(self):
        task_id = uuid.uuid4()
        task = TaskModel(
            task_id,
            scheduled=datetime.datetime.now(),
            task_type='send_gmail',
            invoke_method='SNS',
            call_arn_url='arn:aws:sns:us-east-1:00000000:test',
            data={},
        )
        repo = TaskRepository()
        repo.add_task(task)

        passed = True
        try:
            task_executer(event={}, context={})
        except:
            passed = False

        self.assertTrue(passed, 'Execute SNS task with CloudWatch failed.')


if __name__ == '__main__':
    unittest.main()