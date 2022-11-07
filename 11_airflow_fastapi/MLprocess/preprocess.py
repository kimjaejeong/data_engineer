import numpy as np
import pandas as pd
from copy import copy
from numpy import nan
import openpyxl

class CoronaPreprocess:
    def __init__(self):
        pass

    def run_preprocessing(self, data_url, excel_url):
        data = self._load_df(data_url,excel_url)
        data = self._change_type(data)
        data = self._set_index(data)
        data = self._delete_col(data)
        return data

    def _load_df(self,data_url,excel_url):
        data = pd.read_excel(data_url+excel_url)
        print(data)
        return data
    
    def _change_type(self, result):
        result['createdt'] = pd.to_datetime(result["createdt"])
        # 오브젝트를 숫자로 바꾸기
        result['incdec']       = pd.to_numeric(result['incdec'])
        result['deathcnt']     = pd.to_numeric(result['deathcnt'])
        result['defcnt']       = pd.to_numeric(result['defcnt'])
        #result['isolClearCnt'] = pd.to_numeric(result['isolClearCnt'])
        #result['isolIngCnt']   = pd.to_numeric(result['isolIngCnt'])
        result['localocccnt']  = pd.to_numeric(result['localocccnt'])
        result['overflowcnt']  = pd.to_numeric(result['overflowcnt'])
        return result

    
    def _set_index(self,result):
        # 총 합계만 남기기
        result_total = result[result["gubuncn"] == '合计'].reset_index(drop=True)
        return result_total

    def _delete_col(self,result):
        result.drop(['stdday', 'gubuncn', 'gubunen', 'seq','Unnamed: 0'], axis=1, inplace=True)
        return result