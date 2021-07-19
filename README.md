# data_engineer
data_engineer 관련 소스 정리

- 데이터 읽어들이기 - chunksize

  - https://github.com/kimjaejeong/data_engineer/blob/main/jupyer/01_large_capacity.ipynb

- 병렬 처리

  \- pyspark

  - 정의

    - 범용 분산 데이터 처리 엔진
    - 대규모 및 고속 빅 데이터 처리에 특히 유용
    - Spark는 분산 친화적

  - 특징

    - RAM에서 발생하게 설정 가능
    - Lazy execution을 통해 보다 효율적인 처리/분석이 가능
      - Lazy Execution은 함수를 Transform, Action 으로 구분해 Action 일 경우에만 실제 실행이 발생하는 것
      - 매번 결과를 갖고 오지 않고, 필요한 경우에만 RAM을 통해 데이터 I/O가 발생하므로 분석 작업 속도가 매우 높아짐
    - 스파크는 분산처리프레임 위에 Spark Streaming, SparkSQL, MLlib, GraphX와 같은 모듈을 제공하여 실시간 수집부터 데이터 추출/전처리, 머신러닝 및 그래프 분석까지 하나의 흐름에 가능하도록 개발
    - 인 메모리 작업으로 인해 기존 Hadoop MapReduce 보다 최대 100 배 더 빠르며 , 강력하고 분산 된 내결함성 데이터 객체 (라고 함)를 제공하며 Mlib 와 같은 보충 패키지를 통해 기계 학습 및 그래프 분석의 세계와 아름답게 통합

  - 장점

    - 데이터 파티셔닝 및 작업 관리의 모든 복잡성이 뒤에서 자동으로 처리되고 프로그래머가 특정 분석 또는 기계 학습 작업 자체에 집중 가능

  - 활용

    - 다양한 분석 API 제공
    - pyspark는 DB, list처럼 데이터 묶음이 있을때 이를 병렬로 처리해서 속도를 빨리 처리해주는 역할
    - 매트릭스 연산과 비슷

  - 참고 자료

    - https://frhyme.github.io/python-lib/pyspark/

      (pyspark 개념 설명 및 예제 참고자료)

    - https://wikidocs.net/16565

      (Spark 개념 설명)

  - spark 설치