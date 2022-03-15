# Airflow
- 참고 url
  - https://dydwnsekd.tistory.com/56
  - https://www.youtube.com/watch?v=aTaytcxy2Ck
- airflow에서 제공하는 docker-compose.yml을 다운로드 
```bash
- curl -LfO 'http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/docker-compose.yaml'
- echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
- mkdir ./dags ./logs ./plugins
- docker-compose up airflow-init
- docker-compose up -d # 백그라운드로 실행해줘야 함. / d를 안하면 서버가 계속 돌아가고 있음
- docker-compose down && docker-compose up -d # 재기동
```

- 처음 계정
  - id: airflow / pwd: airflow


```bash
- test
  - curl -X GET --user "airflow:airflow" "http://localhost:8080/api/v1/dags"

```
