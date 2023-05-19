import numpy    as np
# OLS를 하기 위한 라이브러리
import statsmodels.api as sm
# from statsmodels import api as sm
import pandas as pd

class coronaDataModeling:
    def __init__(self):
        self.step = 1  # 다음 값을 찾을 때 증가하는 값
        self.interval = []
        self.a1 = 0  # 초기값
        self.a2 = 14  # 최소 구간 : 각 구간의 최소 간격
        self.p_alpha = 0.8
        self.targets = "temp"
        self.predict="temp"

    def _ols_model(self, data):
        self._set_interval(data)
        self._model_training()

    def _set_interval(self, data):
        self.target = data["incdec"]
        tt = self.target.iloc[self.a1:self.a2]

        trend = range(len(tt))  # 데이터프레임으로 바꿔서 준비
        trend_t = pd.DataFrame({"trend_0": trend})
        trend_line = sm.add_constant(trend_t, has_constant="add")
        lin_scan = sm.OLS(tt, trend_line)
        fitted_lin_scan = lin_scan.fit()
        para_t = fitted_lin_scan.params
        conf_t = fitted_lin_scan.conf_int(alpha=self.p_alpha, cols=None)
        para_0 = para_t["trend_0"]
        conf0_0 = conf_t[0]["trend_0"]
        conf1_0 = conf_t[1]["trend_0"]
        for ii in range(0, len(self.target) - self.a2):
            # 초기값 설정하기
            b1 = self.a1
            b2 = self.a2 + ii * self.step
            if b2 > len(self.target):
                break

            # 목적변수...
            btt = self.target.iloc[b1:b2].reset_index(drop=True)  # index를 초기화 해줘야 새로 만든 트렌드와 붙는다.
            btrend = range(len(btt))
            btrend_t = pd.DataFrame({"trend_0": btrend})
            btrend_line = sm.add_constant(btrend_t, has_constant="add")
            blin_scan = sm.OLS(btt, btrend_line)
            bfitted_lin_scan = blin_scan.fit()
            bpara_t = bfitted_lin_scan.params
            bconf_t = bfitted_lin_scan.conf_int(alpha=self.p_alpha, cols=None)
            bpara_0 = bpara_t["trend_0"]
            bconf0_0 = bconf_t[0]["trend_0"]
            bconf1_0 = bconf_t[1]["trend_0"]
            if (bpara_0 >= conf0_0) & (bpara_0 <= conf1_0):
                b2 = b2 + ii * self.step
            else:
                self.interval.append(b2)
                print(self.interval[-1], '현재 구간값(' + str(ii) + ')')
                a1 = b2
                a2 = a1 + 14
                tt = self.target.iloc[a1:a2].reset_index(drop=True)  # index를 초기화 해줘야 새로 만든 트렌드와 붙는다.
                trend = range(len(tt))
                trend_t = pd.DataFrame({"trend_0": trend})
                trend_line = sm.add_constant(trend_t, has_constant="add")
                lin_scan = sm.OLS(tt, trend_line)
                fitted_lin_scan = lin_scan.fit()
                para_t = fitted_lin_scan.params
                conf_t = fitted_lin_scan.conf_int(alpha=self.p_alpha, cols=None)
                para_0 = para_t["trend_0"]
                conf0_0 = conf_t[0]["trend_0"]
                conf1_0 = conf_t[1]["trend_0"]

    def _model_training(self):
        # 전체 추세...
        trend = range(len(self.target))
        # 데이터프레임으로 바꿔서 준비
        trend_1 = pd.DataFrame({"trend_0": trend})
        inte_0 = self.interval

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
        for i in range(len(self.interval)):
            inter_list.append('int_' + str(self.interval[i]))

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
        trend_lin_001 = sm.OLS(self.target, trend_line)
        fitted_trend_lin_001 = trend_lin_001.fit()
        #print(fitted_trend_lin_001.summary())
        self.predict=fitted_trend_lin_001.fittedvalues
