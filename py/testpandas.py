import pandas as pd

data = pd.read_excel("C:\\software\\test.xls", sheet_name='Sheet1')
data.rename(columns={'ttt': '下单日期'}, inplace=True)
# data.dropna(axis=0, how='all')
data['下单日期'] = data['下单日期'].dt.strftime('%Y/%m/%d')
# data['下单日期'] = data['下单日期'].apply(str)

data.to_excel("C:\\software\\test1.xls", sheet_name='Sheet1', index=False)