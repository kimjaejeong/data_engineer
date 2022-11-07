from urllib.parse            import urlencode, quote_plus,unquote
import datetime

class PathConfig:
    def __init__(self):
        self.url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
        self.API_key = unquote(
            'CSlsJLVnvhYY4H%2FCPCYrOHHzIOXx5jIJpTFowFfKOaIF%2FCXihOa%2B1DKa7gSisitp97bLYaUoEstJxHCrOg4MPg%3D%3D')
        self.dataUrl="data/"
        now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.exceldataname='01_date_colona_'+now_date+'.xlsx'
        self.sdate= datetime.datetime(2020, 4, 9)
        self.now=datetime.datetime.now()

    def get_queryParams(self):
        now = datetime.datetime.now()
        formattedtoday = now.strftime("%Y%m%d")
        queryParams = '?' + urlencode({quote_plus('serviceKey'): self.API_key,
                                       quote_plus('pageNo'): '1',
                                       quote_plus('numOfRows'): '10',
                                       quote_plus('startCreateDt'): '20200409',  # 시작일 : 더 빠른 데이터도 있으나, 포맷이 안 맞음
                                       quote_plus('endCreateDt'): formattedtoday})  # 종료일

        return queryParams
