import pandas as pd 
import time
# 读取时间序列价格表
df = pd.read_excel('DatePrice.xlsx',engine='openpyxl')
# 求每件商品的均值、众数、众数比方差和618当天数据
navg = []
nzhoshu = []
e_ans = []
six18 = []

for i in range(0,480):
    ndf = df.iloc[:,[2*i,2*i+1]]
    avg = 0
    max_day = 0
    all_day = 0
    e = 0
    for j in range(0,len(ndf)-1):
        t1 = time.mktime(time.strptime(str(ndf.iloc[j,0]), '%Y-%m-%d'))
        # 如果达到最终的日期则结束
        if t1 == 1626451200:
            break
        t2 = time.mktime(time.strptime(str(ndf.iloc[j+1,0]), '%Y-%m-%d'))
        # 如果日期间隔中包含了618，则记录价格
        if t2 > 1623945600 and t1 <= 1623945600:
            six18.append(ndf.iloc[j,1])
        # 计算时间相差的天数
        day = (t2-t1)/86400
        # 相差最大天数的价格即为众数
        if max_day < day:
            max_day = day
            zhoshu = ndf.iloc[j,1]
        # 对小于众数的价格求方差之和
        if ndf.iloc[j,1] < zhoshu:
            e = e+day*((zhoshu-ndf.iloc[j,1])/zhoshu)*((zhoshu-ndf.iloc[j,1])/zhoshu)
        # 总天数+1
        all_day = all_day+day
        # 价格求和
        avg = avg + ndf.iloc[j,1]*(t2-t1)/86400
    # 求均值
    avg = avg/all_day
    # 加入列表
    navg.append(avg)
    nzhoshu.append(zhoshu)
    e_ans.append(e)

# 生成dataframe类对象
result = pd.DataFrame({'平均价格':navg,'众数':nzhoshu,'小于众数的方差':e_ans,'618当天价格':six18})
# 写入excel
result.to_excel('statistical.xlsx',sheet_name='商品统计')
    
        