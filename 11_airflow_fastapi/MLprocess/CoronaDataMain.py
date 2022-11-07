

#from preprocess import TitanicPreprocess
from config import PathConfig
from dataio import DataIOSteam
from preprocess import CoronaPreprocess
from model import coronaDataModeling
from visualize_graph import VisualizeProcess

class CoronaDataMain(PathConfig,DataIOSteam,CoronaPreprocess, VisualizeProcess, coronaDataModeling):

    def __init__(self):
        PathConfig.__init__(self)
        DataIOSteam.__init__(self)
        CoronaPreprocess.__init__(self)
        coronaDataModeling.__init__(self)

    def save_excel_from_url(self):
        queryParams=self.get_queryParams()
        df = self.get_data(self.url, queryParams)
        file_name = self.save_excel_data(self.dataUrl,self.exceldataname,df)
        return file_name

    def preprocess_data(self):
        data=self.run_preprocessing(self.dataUrl,self.exceldataname)
        return data

    def visualize(self, df):
        self.training_val_loss(df,self.sdate,self.now)

    def model1(self, df):
        result = self._ols_model(df)
        return result

    def visual_result(self,df):
        self.draw_result(df,self.predict)

    def model2(self, df):
        y_train, y_test, x_train, x_test, x_val, partial_x_train, y_val, partial_y_train = self.train_data_define(df)

        history, model = self.assign_simpple_kerasModel(df, y_train, y_test, x_train, x_test, x_val, partial_x_train, y_val,
                                            partial_y_train)
        # data = self.run_preprocessing(data)
        return history, model

    def check_model(self, history, model):
        self.training_val_loss(history)
        self.training_acc(history)
        self.train_acc_loss(history)

    def prepro_data3(self,f_name1, f_name2, **kwargs):

        #dataIO로 data1과 data2를 받아옴,,
        data1 = self.get_data(self.data_path, f_name1)
        data2 = self.get_data(self.data_path, f_name2)
        #preprocess화
        data = self.run_preprocessing(data1, data2)
        data3 = self.assign_3(data)
        return data3