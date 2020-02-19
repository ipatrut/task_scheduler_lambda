import os
import sys
import json
import logging
from repositories.task import TaskModel, TaskRepository
from utils.api_utils import get_path_parameters, get_query_parameters

logging.basicConfig(level=logging.DEBUG)

def get_tasks(event, context):
    logging.info('event: {}'.format(event))
    params = get_query_parameters(event)

    try:
        repo = TaskRepository()

        if params is None:
            tasks = repo.get_all_tasks()
        elif 'type' in params:
            tasks = repo.get_tasks_by_task_type(params['type'])
        elif 'from' in params and 'to' in params:
            tasks = repo.get_tasks_by_created(params['from'], params['to'])
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Bad parameter(s) in query string'
                })
            }

        items = []
        for task in tasks:
            items.append(task.__dict__)

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except Exception as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                    'error': 'Internal Error: {}'.format(e)
                })
        }


def add_task(event, context):
    logging.info('event: {}'.format(event))

    try:
        body = get_body(event)
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Bad parameter(s) in request'
            })
        }       

    try:
        task = TaskModel(
            scheduled=body['scheduled'],
            task_type=body['task_type'],
            invoke_method=body['invoke_method'],
            call_arn_url=body['call_arn_url'],
            parameters=body['parameters'],
            data=body['data'])

        repo = TaskRepository()
        repo.add_task(task)

        return {
            'statusCode': 200,
            'body': json.dumps(task.__dict__)
        }
    except Exception as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                    'error': 'Internal Error: {}'.format(e)
                })
        }


def modify_task(event, context):
    logging.info('event: {}'.format(event))

    try:
        body = get_body(event)
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Bad parameter(s) in request'
            })
        }

    try:
        repo = TaskRepository()
        task = repo.get_task_by_task_id(body['task_id'])

        if task is None:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Entry not found'
                })
            }

        for key, value in body:
            setattr(task, key, value)

        repo.update_task(task)
        return {
            'statusCode': 200,
            'body': json.dumps(task.__dict__)
        }
    except Exception as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal Error: {}'.format(e)
            })
        }


def get_by_id(event, context):
    """
    Get a task by id
    """
    logging.info('event: {}'.format(event))

    params = get_path_parameters(event)

    try:
        repo = TaskRepository()
        task = repo.get_task_by_task_id(params['id'])

        if task is None:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Entry not found'
                })
            }

        return {
            'statusCode': 200,
            'body': json.dumps(task.__dict__)
        }
    except Exception as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                    'error': 'Internal Error: {}'.format(e)
                })
        }


def delete_by_id(event, context):
    """
    Delete task by id
    """
    logging.info('event: {}'.format(event))

    params = get_path_parameters(event)

    try:
        repo = TaskRepository()
        task = repo.get_task_by_task_id(params['id'])
        if task is None:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Entry not found'
                })
            }

        repo.delete_task_by_task_id(task.task_id)
        return {
            'statusCode': 204
        }
    except Exception as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                    'error': 'Internal Error: {}'.format(e)
                })
        }

if __name__ == "__main__":
    pass
