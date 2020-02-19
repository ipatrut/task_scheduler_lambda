import os
import sys
import json
import uuid
import logging
import datetime
from repositories.task import TaskModel, TaskRepository

def handler(event, context):
    logging.info('event: {}'.format(event))

    message = json.loads(event['Records'][0]['Sns']['Message'])
    method = message['method']
    body = message['body']

    repo = TaskRepository()
    if message['method'] == 'ADD':
        task = TaskModel(
            task_id=uuid.uuid4(),
            scheduled=datetime.datetime.strptime(body['scheduled'], '%Y-%m-%d %H:%M:%S'),
            task_type=body['task_type'],
            invoke_method=body['invoke_method'],
            call_arn_url=body['call_arn_url'],
            parameters=body['parameters'],
            data=body['data'])
        repo.add_task(task)

    elif method == 'UPDATE':
        task = repo.get_task_by_task_id(body['task_id'])

        if task is not None:
            for key, value in body.items():
                setattr(task, key, value)
            repo.update_task(task)
        else:
            logging.error('Entry not found')

    elif method == 'DELETE':
        task = repo.get_task_by_task_id(body['id'])
        if task is not None:
            repo.delete_task_by_task_id(task.task_id)
        else:
            logging.error('Entry not found')

    else:
        logging.error('Unknown method')
