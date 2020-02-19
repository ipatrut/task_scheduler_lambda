import os
import sys
import json
import boto3
import requests
import logging
from repositories.task import TaskModel, TaskRepository
from botocore.exceptions import ClientError


def handler(event, context):
    logging.info('event: {}'.format(event))

    repo = TaskRepository()
    pending_tasks = repo.get_pending_tasks()

    for task in pending_tasks:
        if task.invoke_method == 'REST':
            logging.info("Invoke REST API: {}".format(task.call_arn_url))
            requests.post(task.call_arn_url, data = json.loads(task.data), headers={'Content-type': 'application/json'})
            task.invoked = True

        elif task.invoke_method == 'SNS':
            logging.info("Publish SNS notification: {}".format(task.call_arn_url))
            sns = boto3.client('sns', region_name=os.environ['REGION'])
            try:
                sns.publish(TopicArn=task.call_arn_url, Message=task.parameters)
            except ClientError:
                logging.error('Invalid ARN: {}'.format(task.call_arn_url))
            task.invoked = True

        else:
            logging.error('Unknown Task: {}'.format(task.task_id))
            task.active = False

        repo.update_task(task)
