import boto3

glue_client = boto3.client(service_name='glue',
                           region_name='ap-northeast-1',
                           endpoint_url='https://glue.ap-northeast-1.amazonaws.com',
                           aws_access_key_id='',
                           aws_secret_access_key='',
                           )

response = glue_client.create_database(
    DatabaseInput={
        'Name': 'test-db'
    }
)

# 크롤러 생성(테이블도 같이 생성)
# Role : IAM 역할 생성
response = glue_client.create_crawler(
    Name='test-crawler',
    Role='AWSGlueServiceRoleDefault',
    DatabaseName='test-db',
    Description='string',
    Targets={
        'S3Targets': [
            {
                'Path': '',
                'Exclusions': [
                ]
            }
        ]
    },
    TablePrefix='test_',
    SchemaChangePolicy={
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'DELETE_FROM_DATABASE'
    }
)

response = glue_client.start_crawler(
    Name='test-crawler'
)

# Job 생성(CSV 데이터를 데이터베이스로 변환하는 작업)
response = glue_client.create_job(
    Name='test-job',
    Description='string',
    Role='AWSGlueServiceRoleDefault',
    Command={
        'Name': 'glueetl',
        'ScriptLocation': ''
    }
)

response = glue_client.start_job_run(
    JobName='test-job'
)
