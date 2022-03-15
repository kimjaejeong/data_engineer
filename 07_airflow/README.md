# Airflow
- 참고 url
  - https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html
      - 공식 홈페이지
  - https://dydwnsekd.tistory.com/56
  - https://www.youtube.com/watch?v=aTaytcxy2Ck
    - 기본 강의
  
- airflow에서 제공하는 docker-compose.yml을 다운로드 
```bash
- curl -LfO 'http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/docker-compose.yaml'
- echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
- mkdir ./dags ./logs ./plugins
- docker-compose up airflow-init
- docker-compose down && docker-compose up -d # 재기동
```

- 처음 계정
  - id: airflow / pwd: airflow


```bash
- test
  - curl -X GET --user "airflow:airflow" "http://localhost:8080/api/v1/dags"

```

