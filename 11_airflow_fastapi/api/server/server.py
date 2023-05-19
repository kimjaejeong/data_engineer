# from pandas.core.frame import DataFrame
from fastapi import FastAPI, Body
import pandas as pd
import requests, bs4
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
from lxml import html
import datetime

import numpy    as np
# OLS를 하기 위한 라이브러리
import statsmodels.api as sm
# from statsmodels import api as sm

app = FastAPI()

def covidData(url, queryParams):
    # 서비스 url 과 파라메터 묶기
    request = Request(url + queryParams)
    # 호출 방법 : 여기서는 GET
    request.get_method = lambda: 'GET'
    # 결과값 받아내서 UTF-8로 읽기
    response_body = urlopen(request).read().decode('utf-8')
    # 문자 부분만 추출하기
    root = ET.fromstring(response_body)
    # xml 디버깅용 오브젝트로 넣기
    xmlobj = bs4.BeautifulSoup(response_body, 'lxml-xml')
    # item 부분만 남기기
    rows = xmlobj.findAll('item')

    # 모든 행과 열의 값을 모아 매트릭스로 만들어보자.
    rowList = []
    nameList = []
    columnList = []

    rowsLen = len(rows)

    for i in range(0, rowsLen):
        columns = rows[i].find_all()

        columnsLen = len(columns)
        for j in range(0, 12):
            #    for j in range(0, columnsLen):
            # 첫 번째 행 데이터 값 수집 시에만 컬럼 값을 저장한다.
            # (어차피 rows[0], rows[1], ... 모두 컬럼헤더는 동일한 값을 가지기 때문에 매번 반복할 필요가 없다.)
            # 그런데 꼭 같은 헤더를 가지는 것은 아니다. 시점에 따라서, 응답값이 바뀌기도 한다...
            if i == 0:
                nameList.append(columns[j].name)
            # 컬럼값은 모든 행의 값을 저장해야한다.
            eachColumn = columns[j].text
            columnList.append(eachColumn)
        rowList.append(columnList)
        columnList = []  # 다음 row의 값을 넣기 위해 비워준다. (매우 중요!!)
    result = pd.DataFrame(rowList, columns=nameList)
    return result

def olsModel(result):
    # 오브젝트를 날짜 형식으로 바꾸기
    result['createDt'] = pd.to_datetime(result["createDt"])
    # 오브젝트를 숫자로 바꾸기
    result['incDec'] = pd.to_numeric(result['incDec'])
    result['deathCnt'] = pd.to_numeric(result['deathCnt'])
    result['defCnt'] = pd.to_numeric(result['defCnt'])
    # result['isolClearCnt'] = pd.to_numeric(result['isolClearCnt'])
    # result['isolIngCnt']   = pd.to_numeric(result['isolIngCnt'])
    result['localOccCnt'] = pd.to_numeric(result['localOccCnt'])
    result['overFlowCnt'] = pd.to_numeric(result['overFlowCnt'])

    # 총 합계만 남기기
    result_total = result[result["gubunCn"] == '合计'].reset_index(drop=True)
    # result_total

    ymax = max(result_total.incDec)  # 최대값을 표시해주려했는데, 44,200이 들어와서...

    # 세로 가이드라인을 넣는데, 시작일을 잡아줘야 한다.
    sdate = datetime.datetime(2020, 4, 9)

    # 너무 길게 보이지 않도록... 몇 개 의미 없는 컬럼을 없애고...
    result_total.drop(['stdDay', 'gubunCn', 'gubunEn'], axis=1, inplace=True)

    x = result_total["createDt"]  # 기준일
    y = result_total["incDec"]  # 신규 확진자 수
    y1 = result_total["overFlowCnt"]  # 신규 확진자 수

    target = y  # 목적변수 = 신규 확진자 수
    interval = []  # 결과값 모을 준비
    step = 1  # 다음 값을 찾을 때 증가하는 값
    a1 = 0  # 초기값
    a2 = 14  # 최소 구간 : 각 구간의 최소 간격
    p_alpha = 0.8  # 구간추정의 1 - p-value ~ 작을수록 넓게 잡힘

    tt = target.iloc[a1:a2]

    trend = range(len(tt))  # 데이터프레임으로 바꿔서 준비
    trend_t = pd.DataFrame({"trend_0": trend})
    trend_line = sm.add_constant(trend_t, has_constant="add")
    lin_scan = sm.OLS(tt, trend_line)
    fitted_lin_scan = lin_scan.fit()
    para_t = fitted_lin_scan.params
    conf_t = fitted_lin_scan.conf_int(alpha=p_alpha, cols=None)
    para_0 = para_t["trend_0"]
    conf0_0 = conf_t[0]["trend_0"]
    conf1_0 = conf_t[1]["trend_0"]
    for ii in range(0, len(target) - a2):
        # 초기값 설정하기
        b1 = a1
        b2 = a2 + ii * step
        if b2 > len(target):
            break

        # 목적변수...
        btt = target.iloc[b1:b2].reset_index(drop=True)  # index를 초기화 해줘야 새로 만든 트렌드와 붙는다.
        btrend = range(len(btt))
        btrend_t = pd.DataFrame({"trend_0": btrend})
        btrend_line = sm.add_constant(btrend_t, has_constant="add")
        blin_scan = sm.OLS(btt, btrend_line)
        bfitted_lin_scan = blin_scan.fit()
        bpara_t = bfitted_lin_scan.params
        bconf_t = bfitted_lin_scan.conf_int(alpha=p_alpha, cols=None)
        bpara_0 = bpara_t["trend_0"]
        bconf0_0 = bconf_t[0]["trend_0"]
        bconf1_0 = bconf_t[1]["trend_0"]
        if (bpara_0 >= conf0_0) & (bpara_0 <= conf1_0):
            b2 = b2 + ii * step
        else:
            interval.append(b2)
            print(interval[-1], '현재 구간값(' + str(ii) + ')')
            a1 = b2
            a2 = a1 + 14
            tt = target.iloc[a1:a2].reset_index(drop=True)  # index를 초기화 해줘야 새로 만든 트렌드와 붙는다.
            trend = range(len(tt))
            trend_t = pd.DataFrame({"trend_0": trend})
            trend_line = sm.add_constant(trend_t, has_constant="add")
            lin_scan = sm.OLS(tt, trend_line)
            fitted_lin_scan = lin_scan.fit()
            para_t = fitted_lin_scan.params
            conf_t = fitted_lin_scan.conf_int(alpha=p_alpha, cols=None)
            para_0 = para_t["trend_0"]
            conf0_0 = conf_t[0]["trend_0"]
            conf1_0 = conf_t[1]["trend_0"]

    # 전체 추세...
    trend = range(len(y))
    # 데이터프레임으로 바꿔서 준비
    trend_1 = pd.DataFrame({"trend_0": trend})

    inte_0 = interval

    aa = len(inte_0) + 1

    trend_mul = trend_1
    trend_mul = trend_mul.rename(columns={"trend_0": "tren_1"})

    for ii in range(2, aa):
        trend_mul = pd.concat([trend_mul
                                  , trend_1
                               ]
                              , axis=1
                              )
        trend_mul = trend_mul.rename(columns={'trend_0': 'tren_' + str(ii)})
    # 이렇게 하면, 인터셉트 더미가 알파벳으로만 만들어져서, 26개가 넘어갈 경우 특수문자가 나타남...
    # dum = pd.DataFrame(np.zeros((len(trend), aa-1)), columns=list(map(chr, range(65, 64 + aa))) )

    # 빈 공간을 남겨서, 특징점들을 만들어 내는 것으로 변경
    inter_list = []  # 빈 리스트 생성
    for i in range(len(interval)):
        inter_list.append('int_' + str(interval[i]))

    dum = pd.DataFrame(np.zeros((len(trend), aa - 1)), columns=inter_list)

    for tt in range(aa - 1):
        dum.iloc[0:inte_0[tt], tt] = 1

    dff = pd.DataFrame(np.zeros((len(trend), aa - 1)), columns=trend_mul.columns)
    for tt in range(aa - 1):
        dff.iloc[0:inte_0[tt], tt] = 1
    # 데이터프레임을 곱할 때 컬럼명이 같아야...
    rr = dff.rmul(trend_mul)
    # 전 기간을 포함하는 트렌드와 각 구간 트렌드, Intercept 더미까지 붙여주고...
    trend_lin_t = pd.concat([trend_1
                                , dum
                                , rr
                             ]
                            , axis=1
                            )

    # 전 기간에 해당하는 인터셉트 더미 넣어주고...
    trend_line = sm.add_constant(trend_lin_t, has_constant="add")

    # OLS...
    trend_lin_001 = sm.OLS(y, trend_line)
    fitted_trend_lin_001 = trend_lin_001.fit()
    print(fitted_trend_lin_001.summary())

    y1 = pd.DataFrame(fitted_trend_lin_001.fittedvalues, columns=['fittedvalues'])

    titan_c = pd.concat([result_total, y1], axis=1)

    return titan_c

@app.post("/model")
def trainModel(dict_data: dict = Body(...)):
    data = dict_data['data']
    getData = data[0][0]

    titan_c = olsModel(getData)

    return titan_c

@app.post("/get-data")
def getData(dict_data: dict = Body(...)):
    data = dict_data['data']
    pageNo = data[0][0] # 1
    numOfRows = data[0][1] # 10
    startCreateDt = data[0][2] # 20200409
    endCreateDt = data[0][3] # 20221107

    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    API_key = unquote(
        'CSlsJLVnvhYY4H%2FCPCYrOHHzIOXx5jIJpTFowFfKOaIF%2FCXihOa%2B1DKa7gSisitp97bLYaUoEstJxHCrOg4MPg%3D%3D')

    queryParams = '?' + urlencode({quote_plus('serviceKey'): API_key,
                                   quote_plus('pageNo'): pageNo,
                                   quote_plus('numOfRows'): numOfRows,
                                   quote_plus('startCreateDt'): startCreateDt,  # 시작일 : 더 빠른 데이터도 있으나, 포맷이 안 맞음
                                   quote_plus('endCreateDt'): endCreateDt})  # 종료일

    result = covidData(url, queryParams)

    # result.head()
    # ValueError: 13 columns passed, passed data had 14 columns # 2022-02-24 에러
    return result