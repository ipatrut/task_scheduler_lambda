### Deployment & Test Guide

 1. ##### Create and activate the virtualenv, install requirements of project

    `virtualenv env`

    `source env/bin/activate`

    `pip install -r requirements.txt`

 2. ##### Install required serverless packages

    `npm install`


 3. ##### Create `config.json` from `config.example.json` and set AWS region and mysql connection information.
```json
{
    "REGION": "us-east-1",
    "AURORA_DB_HOST": "task-instance-1.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com",
    "AURORA_DB_PORT": "3306",
    "AURORA_DB_NAME": "task",
    "AURORA_DB_USER": "admin",
    "AURORA_DB_PASSWORD": "password"
}
```

4. ##### Deploy services

    `sls deploy -v --stage {stage}`
    
5. ##### How to test

1) ###### Create test config file 'config.test.json' from `config.example.json` and set the variables.

```json
{
    "REGION": "us-east-1",
    "AURORA_DB_HOST": "localhost",
    "AURORA_DB_PORT": "3306",
    "AURORA_DB_NAME": "task",
    "AURORA_DB_USER": "admin",
    "AURORA_DB_PASSWORD": "password"
}
```

2) ###### Run test.

    `python -m unittest`


### Enjoy!

