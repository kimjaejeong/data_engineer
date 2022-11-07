# client
#pageNo: 1
#numOfRows: 10
#startCreateDt: 20200409 # 시작일 : 더 빠른 데이터도 있으나, 포맷이 안 맞음
#endCreateDt:
import pandas as pd
import json
import requests
from datetime import datetime

common_address = 'http://localhost:8080/'

def callData(pageNo, numOfRows, startCreateDt, endCreateDt):
    #### 요약 ########
    headers = {'Content-Type': 'application/json'}
    api_name = "get-data"
    getData_address = common_address + api_name
    request_data = pd.DataFrame([pageNo, numOfRows, startCreateDt, endCreateDt], columns=['pageNo', 'numOfRows', 'startCreateDt', 'endCreateDt'])
    original_payload = {
        'data': request_data.to_numpy().tolist()
    }
    # dataframe 형태로 나옴
    result = requests.post(getData_address, data=json.dumps(original_payload), headers=headers)

    return result

def trainModel(getData):
    #### 요약 ########
    headers = {'Content-Type': 'application/json'}
    api_name = "model"
    trainModel_address = common_address + api_name
    original_data = pd.DataFrame([[getData]], columns=["original_data"])
    original_payload = {
        'data': original_data.to_numpy().tolist()
    }
    result = requests.post(trainModel_address, data=json.dumps(original_payload), headers=headers)
    return result

if __name__ == "__main__":
    # data 불러오기
    pageNo = 1
    numOfRows = 10
    startCreateDt = 20200409
    endCreateDt = datetime.now().strftime("%Y%m%d")

    # 데이터 불러오기 API
    getData = callData(pageNo, numOfRows, startCreateDt, endCreateDt)

    # 데이터 학습 API
    titan_c = trainModel(getData)

    print(titan_c)


