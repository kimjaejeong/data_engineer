# from awsglue.context import GlueContext
# from pyspark.context import SparkContext
# from awsglue.job import Job
# import sys
# from awsglue.utils import getResolvedOptions
# from awsglue.dynamicframe import DynamicFrame

import findspark
findspark.init()
from awsglue.context import GlueContext
from pyspark import SparkContext
sc = SparkContext("local", "first app")

print(sc)
glueContext = GlueContext(SparkContext.getOrCreate())

print(glueContext)
# glueJob = Job(GlueContext)
# args = getResolvedOptions(sys.argv, ['JOB_NAME'])
#
# glueJob.init(args['JOB_NAME'], args)
# sparkSession = glueContext.sparkSession
#
# ## ETL
# user_spark_df = sparkSession.format("jdbc").option("url", "")
#
#
# user_dynamic_df = DynamicFrame.fromDF(
#     user_spark_df,
#     glueContext,
#     "convert_ctx"
# )
#
# glueContext.write_dynamic_frame.from_options(
#     frame = user_dynamic_df,
#     connection_type="s3",
#     connection_options=("path", "s3 경로"),
#     format="parquet",
#     transformation_ctx="transformation_ctx"
# )
#
# glueJob.commit()

