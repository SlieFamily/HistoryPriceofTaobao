import pandas as pd 
import time
# 读取时间序列价格表
df = pd.read_excel('DatePrice.xlsx',engine='openpyxl')
# 求每件商品的众数和均值
navg = []
nzhoshu = []
ans = []
for i in range(0,480):
    ndf = df.iloc[:,[2*i,2*i+1]]
    avg = 0
    max_day = 0
    all_day = 0
    e = 0
    for j in range(0,len(ndf)-1):
        t1 = time.mktime(time.strptime(str(ndf.iloc[j,0]), '%Y-%m-%d'))
        if t1 == 1626451200:
            break
        t2 = time.mktime(time.strptime(str(ndf.iloc[j+1,0]), '%Y-%m-%d'))
        day = (t2-t1)/86400
        if max_day < day:
            max_day = day
            zhoshu = ndf.iloc[j,1]
        if ndf.iloc[j,1] < zhoshu:
            e = e+day*((zhoshu-ndf.iloc[j,1])/zhoshu)*((zhoshu-ndf.iloc[j,1])/zhoshu)
        all_day = all_day+day
        avg = avg + ndf.iloc[j,1]*(t2-t1)/86400
    avg = avg/all_day
    navg.append(avg)
    nzhoshu.append(zhoshu)
    ans.append(e)

result = pd.DataFrame({'平均价格':navg,'众数':nzhoshu,'小于众数的方差':ans})
result.to_excel('statistical.xlsx',sheet_name='商品统计')
    
        