import os
import json
import uuid
import time
import logging
import datetime
import pymysql


class TaskModel:
    def __init__(self,
                 task_id, scheduled,
                 task_type='send_gmail', invoke_method='REST', call_arn_url='',
                 parameters={}, data={}, invoked=False, active=True, created_at=datetime.datetime.utcnow()):

        self.task_id = str(task_id)
        self.created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
        self.scheduled = scheduled.strftime('%Y-%m-%d %H:%M:%S')
        self.task_type = task_type
        self.invoke_method = invoke_method
        self.call_arn_url = call_arn_url
        self.parameters = parameters
        self.data = data
        self.invoked = invoked
        self.active = active


class TaskRepository:
    table_name = 'tasks'

    def __init__(self):
        try:
            self.host = os.environ['AURORA_DB_HOST']
            self.user = os.environ['AURORA_DB_USER']
            self.password = os.environ['AURORA_DB_PASSWORD']
            self.db_name = os.environ['AURORA_DB_NAME']

            self._conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    passwd=self.password,
                    db=self.db_name
                )
            self._cursor = self._conn.cursor(pymysql.cursors.DictCursor)
        except pymysql.err.InternalError:
            try:
                self._conn = pymysql.connect(
                        host=self.host,
                        user=self.user,
                        passwd=self.password
                    )
                self._cursor = self._conn.cursor(pymysql.cursors.DictCursor)
                self.create_db()
                self.create_table()
            except Exception as e:
                logging.error(e)


    def create_db(self):
        sql = 'CREATE DATABASE {};'.format(self.db_name)
        self._execute(sql)
        sql = 'use {};'.format(self.db_name)
        self._execute(sql)

    def create_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                task_id VARCHAR(256) PRIMARY KEY,
                created_at TIMESTAMP  DEFAULT NOW(),
                scheduled TIMESTAMP DEFAULT NOW(),
                task_type VARCHAR(256),
                invoke_method VARCHAR(256),
                call_arn_url VARCHAR(1024),
                parameters JSON,
                data JSON,
                invoked BOOL,
                active BOOL,
                INDEX by_task_id (task_id),
                INDEX by_task_type (task_type),
                INDEX by_created_at (created_at),
                INDEX by_scheduled (scheduled)
            );
            '''.format(TABLE_NAME=self.table_name)
        self._execute(sql)

    def _execute(self, sql):
        self._cursor.execute(sql)
        self._conn.commit()
        return self._cursor.fetchall()

    def add_task(self, task):
        value_list = list(task.__dict__.values())
        values = ', '.join("'{}'".format(str(x)) for x in value_list)
        values = values.replace("'True'", 'True').replace("'False'", 'False')
        sql = '''
                INSERT INTO {TABLE} VALUES({VALUES});
            '''.format(TABLE=self.table_name, VALUES=values)
        self._execute(sql)
        return task

    def update_task(self, task):
        value_list = list(task.__dict__.items())
        value_list.pop(0)
        values = ', '.join("{}='{}'".format(key, str(value)) for key, value in value_list)
        values = values.replace("'True'", 'True').replace("'False'", 'False')

        sql = '''
            UPDATE {TABLE} SET {VALUES} WHERE task_id='{TASK_ID}';
        '''.format(TABLE=self.table_name, VALUES=values, TASK_ID=task.task_id)
        self._execute(sql)
        return task.task_id

    def get_all_tasks(self):
        sql = '''
            SELECT * FROM {TABLE};
        '''.format(TABLE=self.table_name)
        items = self._execute(sql)

        return [
            TaskModel(
                task_id=uuid.UUID(item['task_id']),
                created_at=item['created_at'],
                scheduled=item['scheduled'],
                task_type=item['invoke_method'],
                invoke_method=item['invoke_method'],
                call_arn_url=item['call_arn_url'],
                parameters=item['parameters'],
                data=item['data'],
                invoked=bool(item['invoked'], ),
                active=bool(item['active'], )
            ) for item in items
        ]

    def get_pending_tasks(self):
        sql = '''
            SELECT * FROM {TABLE} WHERE scheduled<NOW() and invoked=False and active=True;
        '''.format(TABLE=self.table_name)
        items = self._execute(sql)

        return [
            TaskModel(
                task_id=uuid.UUID(item['task_id']),
                created_at=item['created_at'],
                scheduled=item['scheduled'],
                task_type=item['invoke_method'],
                invoke_method=item['invoke_method'],
                call_arn_url=item['call_arn_url'],
                parameters=item['parameters'],
                data=item['data'],
                invoked=bool(item['invoked'], ),
                active=bool(item['active'], )
            ) for item in items
        ]


    def get_task_by_task_id(self, task_id):
        sql = '''
            SELECT * FROM {TABLE} WHERE task_id='{TASK_ID}';
            '''.format(TABLE=self.table_name, TASK_ID=task_id)
        items = self._execute(sql)

        if len(items) == 0:
            return None

        item = items[0]
        return TaskModel(
            task_id=uuid.UUID(item['task_id']),
            created_at = item['created_at'],
            scheduled=item['scheduled'],
            task_type=item['invoke_method'],
            invoke_method=item['invoke_method'],
            call_arn_url=item['call_arn_url'],
            parameters=item['parameters'],
            data=item['data'],
            invoked=bool(item['invoked'],),
            active=bool(item['active'],)
        )

    def get_tasks_by_scheduled(self, scheduled_from, scheduled_to):

        sql = '''
            SELECT * FROM {TABLE} WHERE scheduled BETWEEN '{FROM}' AND '{TO}';
        '''.format(TABLE=self.table_name, FROM=scheduled_from, TO=scheduled_to)
        items = self._execute(sql)

        return [
            TaskModel(
                task_id=uuid.UUID(item['task_id']),
                created_at=item['created_at'],
                scheduled=item['scheduled'],
                task_type=item['invoke_method'],
                invoke_method=item['invoke_method'],
                call_arn_url=item['call_arn_url'],
                parameters=item['parameters'],
                data=item['data'],
                invoked=bool(item['invoked'], ),
                active=bool(item['active'], )
            ) for item in items
        ]

    def get_tasks_by_created(self, created_from, created_to):

        sql = '''
            SELECT * FROM {TABLE} WHERE created_at BEETWEEN '{FROM}' AND '{TO}';
            '''.format(TABLE=self.table_name, FROM=created_from, TO=created_to)
        items = self._execute(sql)

        return [
            TaskModel(
                task_id=uuid.UUID(item['task_id']),
                created_at=item['created_at'],
                scheduled=item['scheduled'],
                task_type=item['invoke_method'],
                invoke_method=item['invoke_method'],
                call_arn_url=item['call_arn_url'],
                parameters=item['parameters'],
                data=item['data'],
                invoked=bool(item['invoked'], ),
                active=bool(item['active'], )
            ) for item in items
        ]

    def get_tasks_by_task_type(self, task_type):
        sql = '''
            SELECT * FROM {TABLE} WHERE task_type='{TASK_TYPE}';
            '''.format(TABLE=self.table_name, TASK_TYPE=task_type)
        items = self._execute(sql)

        return [
            TaskModel(
                task_id=uuid.UUID(item['task_id']),
                created_at=item['created_at'],
                scheduled=item['scheduled'],
                task_type=item['invoke_method'],
                invoke_method=item['invoke_method'],
                call_arn_url=item['call_arn_url'],
                parameters=item['parameters'],
                data=item['data'],
                invoked=bool(item['invoked'], ),
                active=bool(item['active'], )
            ) for item in items
        ]

    def delete_task_by_task_id(self, task_id):
        sql = '''
            DELETE FROM {TABLE} WHERE task_id='{TASK_ID}';
        '''.format(TABLE=self.table_name,TASK_ID=task_id)
        self._execute(sql)
