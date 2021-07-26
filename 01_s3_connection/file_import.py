import boto3
import pandas as pd

# Windows - CMD: aws configure
# AWS_ACCESS_KEY_ID = ''
# AWS_ACCESS_KEY_SECRET = ''
# region_name = ''

client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
# my_bucket = resource.Bucket('my-bucket') #subsitute this for your s3 bucket name.

for bucket in resource.buckets.all():
    bucket_name = bucket.name

# obj = client.get_object(Bucket=bucket_name, Key='test.csv')
obj = client.get_object(Bucket=bucket_name, Key='test.csv')
grid_sizes = pd.read_csv(obj['Body'])
print(grid_sizes)

