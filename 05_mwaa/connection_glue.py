## airflow ##
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

## glue ##
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

def print_hello():
    return "Airflow Start~~"

def connection_glue():
    # @params: [JOB_NAME]
    args = getResolvedOptions(sys.argv, ['JOB_NAME'])

    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)

    # @type: DataSource
    # @args: [database = "test-db", table_name = "test_hello_csv", transformation_ctx = "datasource0"]
    # @return: datasource0
    # @inputs: []
    datasource0 = glueContext.create_dynamic_frame.from_catalog(database="test-db", table_name="test_hello1_csv",
                                                                transformation_ctx="datasource0")

    # @type: ApplyMapping
    # @args: [mapping = [("name", "string", "name", "string"), ("age", "long", "age", "long")], transformation_ctx = "applymapping1"]
    # @return: applymapping1
    # @inputs: [frame = datasource0]
    applymapping1 = ApplyMapping.apply(frame=datasource0,
                                       mappings=[("name", "string", "name", "string"), ("age", "long", "age", "long")],
                                       transformation_ctx="applymapping1")
    # @type: SelectFields
    # @args: [paths = ["name", "age"], transformation_ctx = "selectfields2"]
    # @return: selectfields2
    # @inputs: [frame = applymapping1]
    selectfields2 = SelectFields.apply(frame=applymapping1, paths=["name", "age"], transformation_ctx="selectfields2")
    # @type: ResolveChoice
    # @args: [choice = "MATCH_CATALOG", database = "test-db", table_name = "test_hello_csv", transformation_ctx = "resolvechoice3"]
    # @return: resolvechoice3
    # @inputs: [frame = selectfields2]
    resolvechoice3 = ResolveChoice.apply(frame=selectfields2, choice="MATCH_CATALOG", database="test-db",
                                         table_name="test_hello1_csv", transformation_ctx="resolvechoice3")
    # @type: DataSink
    # @args: [database = "test-db", table_name = "test_hello_csv", transformation_ctx = "datasink4"]
    # @return: datasink4
    # @inputs: [frame = resolvechoice3]
    datasink4 = glueContext.write_dynamic_frame.from_catalog(frame=resolvechoice3, database="test-db",
                                                             table_name="test_hello1_csv",
                                                             transformation_ctx="datasink4")
    job.commit()

dag = DAG("hello_glue", description="Simple tutorial DAG",
          schedule_interval="0 12 * * *",
          start_date=datetime(2021, 7, 28), catchup=False
          )

dummy_operator = DummyOperator(task_id = "dummy_task", retries=3, dag = dag)
hello_operator = PythonOperator(task_id="hello_task", python_callable=print_hello, dag = dag)
glue_operator = PythonOperator(task_id="glue_task", python_callable=connection_glue, dag = dag)

dummy_operator >> hello_operator >> glue_operator