import os
import unittest
import datetime
from tests.unit.test_base import UnitTestBase
from repositories.task import TaskModel, TaskRepository
from task_api import get_tasks, get_by_id, add_task, modify_task, delete_by_id


class TestTaskApi(UnitTestBase):
    def test_get_all_tasks(self):
        event = {'queryStringParameters': None}
        response = get_tasks(event, {})
        self.assertEqual(response['statusCode'], 200)


if __name__ == '__main__':
    unittest.main()