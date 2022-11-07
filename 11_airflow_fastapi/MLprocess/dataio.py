

import xml.etree.ElementTree as ET
from urllib.request          import Request, urlopen
import pandas as pd
import bs4
import datetime

class DataIOSteam:

    def get_data(self, url, queryParams):
        # 서비스 url 과 파라메터 묶기
        request = Request(url + queryParams)
        # 호출 방법 : 여기서는 GET
        request.get_method = lambda: 'GET'
        # 결과값 받아내서 UTF-8로 읽기
        response_body = urlopen(request).read().decode('utf-8')
        # 문자 부분만 추출하기
        root = ET.fromstring(response_body)
        # xml 디버깅용 오브젝트로 넣기
        xmlobj = bs4.BeautifulSoup(response_body, 'lxml')
        # item 부분만 남기기
        rows = xmlobj.findAll('item')
        return rows

    def save_excel_data(self, data_dir,filename,rows):
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
        result.to_excel(data_dir + filename )
        return result