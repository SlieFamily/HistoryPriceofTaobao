import pandas as pd

# 读取时间序列价格表
df = pd.read_excel('DatePrice.xlsx',engine='openpyxl')
# 时间序列最长的商品（以此为基准）
base_df = df.iloc[:,[2*312,2*312+1]]

adf = df.iloc[:,[0,1]]

print(len(df))
print(len(base_df))
print(adf.iloc[290,1] == 'nan')