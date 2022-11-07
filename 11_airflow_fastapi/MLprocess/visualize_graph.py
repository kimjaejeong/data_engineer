import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class VisualizeProcess:
    def __init__(self):
        pass

    def check_line(self,df,sdate_t,now):
        # x축, y축 잡아주고...
        x = df["createdt"]  # 기준일
        y = df["incdec"]  # 신규 확진자 수
        y1 = df["overflowcnt"]  # 신규 확진자 수
        ymax = max(df.incdec)
        # 그래프 크기 바꾸고, 그리기...
        plt.figure(figsize=(16, 7))
        plt.rcParams['axes.grid'] = True
        plt.hlines(y=10000, xmin=sdate_t, xmax=now, color='g', linewidth=1, linestyle='-.', )
        plt.hlines(y=25000, xmin=sdate_t, xmax=now, color='y', linewidth=2, linestyle='--', )
        plt.hlines(y=50000, xmin=sdate_t, xmax=now, color='r', linewidth=3, linestyle='--', )
        plt.hlines(y=ymax, xmin=sdate_t, xmax=now, color='r', linewidth=1,)
        # plt.hlines(y=ymax, xmin = sdate_t, xmax = now, color='r', linewidth=3,)
        # 이게 44200이 들어와서 제대로 작동 안 한다...
        plt.xlim(sdate_t, now)
        # plt.ylim(0,8000)  # 2021-12-01. 2021=01-04에 이상 정포
        plt.plot(x, y, 'r-', label="신규 확진자 수")
        plt.plot(x, y1, 'b-', label="해외유입 확진자 수")
        plt.show()

    def draw_result(self, data, result):
        y1 = pd.DataFrame(result, columns=['fittedvalues'])
        titan_c = pd.concat([data, y1], axis=1)

        fig = px.line(titan_c
                      , x='createdt'
                      , y=['incdec', 'fittedvalues']
                      , title='Time Series')

        print(data['incdec'])
        print(result)
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        fig.update_xaxes(rangeslider_visible=True)
        fig.show()
