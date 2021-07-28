import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

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
                                                         table_name="test_hello1_csv", transformation_ctx="datasink4")

# to S3 => Parquet 압축 및 S3 저장
# Write out the dynamic frame into parquet in "legislator_history" directory
glueContext.write_dynamic_frame.from_options(frame = resolvechoice3,
          connection_type = "s3",
          connection_options = {"path": "s3://glue-target-sample/output-dir/legislator_history"},
          format = "parquet")

# Write out a single file to directory "legislator_single"
s_history = resolvechoice3.toDF().repartition(1)
s_history.write.parquet('s3://glue-target-sample/output-dir/legislator_single')

job.commit()
