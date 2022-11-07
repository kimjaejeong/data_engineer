from CoronaDataMain import *

ex_1 = CoronaDataMain()
#data = ex_1.save_excel_from_url()
data=ex_1.preprocess_data()
#ex_1.visualize(data)
result=ex_1.model1(data)
ex_1.visual_result(data)