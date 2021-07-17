import pandas as pd 
import time
# 读取时间序列价格表
df = pd.read_excel('DatePrice.xlsx',engine='openpyxl')
# 时间序列最长的商品（以此为基准）
base_df = df.iloc[:,[2*312,2*312+1]]
# 将基准时间填充至新df中
new_df = {}
new_df['时间']=base_df.iloc[:,0]
for i in range(0,480):
    # 两列为单位一一比对
    adf = df.iloc[:,[2*i,2*i+1]]
    k = 0
    new_df[f'商品{i}'] = []
    for j in range(0,len(base_df)):
        t0 = time.mktime(time.strptime(str(base_df.iloc[j,0]), '%Y-%m-%d'))
        # 遍历所有区间
        while k < 291:
            if k == 290:
                break
            elif str(adf.iloc[k+1,1]) == 'nan':
                break
            t1 = time.mktime(time.strptime(str(adf.iloc[k,0]), '%Y-%m-%d'))
            t2 = time.mktime(time.strptime(str(adf.iloc[k+1,0]), '%Y-%m-%d'))
            # 基准时间如果在区间内则填充数据否则更换下一个区间
            if t0 >= t1 and t0 < t2:
                new_df[f'商品{i}'].append(adf.iloc[k,1])
                break
            else:
                k = k+1
    # 别忘记把最后一天加上
    new_df[f'商品{i}'].append(adf.iloc[k,1])

result = pd.DataFrame(new_df)
result.to_excel('arrangeTimeline.xlsx')
        