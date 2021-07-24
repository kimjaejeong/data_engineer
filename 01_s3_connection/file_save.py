import boto3 # S3 Client 생성

def create_bucket(bucket_name):
    # s3 연결
    s3 = boto3.client('s3')  # S3에있는 현재 버킷리스트의 정보를 가져온다.
    # 버킷 리스트 조회
    response = s3.list_buckets()  # response에 담겨있는 Buckets의 이름만 가져와 buckets 변수에 배열로 저장.
    buckets = [bucket['Name'] for bucket in response['Buckets']]  # S3 버킷 리스트를 출력.
    print("Bucket List: %s" % buckets)

    if bucket_name not in buckets:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
        print("버킷 생성 완료")

def upload_file(file_name, bucket_name):
    # s3 연결
    s3 = boto3.client('s3')  # S3에있는 현재 버킷리스트의 정보를 가져온다.

    #로컬에서 올릴 파일이름 / S3 버킷 이름 / 버킷에 저장될 파일 이름
    s3.upload_file(file_name, bucket_name, file_name)

def main():
    bucket_name = 'news-crawling-test'
    file_name = "naver_news_multi.csv"

    # 버킷 생성
    create_bucket(bucket_name)

    # 파일 업로드
    upload_file(file_name, bucket_name)

if __name__ == "__main__":
    main()

    print("파일 업로드 완료")