import requests
import re
import time
import pandas as pd

# 设置请求头
headers = {
	'User-Agent':'Mozilla/5.0',
    'Cookie':'guid=f4664b1dd5a6ff9570dce51a8081e329; __utmc=188916852; PHPSESSID=q0jfjj73rpf41nmcqekc0hait2; Hm_lvt_7705e8554135f4d7b42e62562322b3ad=1626429961,1626430484; __utmz=188916852.1626430485.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; fp=37ecda15d00b76608e403f503b3a1e92; index_big_banner=1; __utma=188916852.1675900409.1626429962.1626430485.1626437223.3; __utmb=188916852.5.10.1626437223; Hm_lpvt_7705e8554135f4d7b42e62562322b3ad=1626437260; dfp=0H88kUZe0CTQ6z8V6CtM6U0+kU0G6H8i0VJM0z82EVPM0CJM0W82EVZM0H820UZM0UM=EUZ86Ut80c55'
}

# 读取excel获取商品ID
df = pd.read_excel('GoodsInf.xlsx',engine='openpyxl')
# 保存各个商品的价格变化字典
ndf = []

# 利用网站的api得到历史价格数据
for j in range(0,len(df)):
    api = f"https://www.gwdang.com/trend/data_www?&dp_id={str(df['商品id'][j])}-83&show_prom=true&v=2"
    # 初始化表单
    Date = []
    Price = []
    # 发起get请求
    res = requests.get(url=api,headers=headers)
    if res.status_code == 200 :
        print('第'+str(j)+'件商品 历史价格爬取中……')
        datePrice = res.json()['series'][0]['data']
        # 规格化数据
        for i in range(0,len(datePrice)):
            Date.append(time.strftime("%Y-%m-%d", time.localtime(datePrice[i]['x'])))
            Price.append(0.01*datePrice[i]['y'])
        totall = {f"{j}-时间":Date,f"{j}-商品价格":Price}
        totall = pd.DataFrame(totall)
        ndf.append(totall)
    else:
        print('错误：',res.status_code)

    # 停留1s
    time.sleep(1)

# 写入excel
result = pd.concat(ndf,axis=1)
result.to_excel('DatePrice.xlsx')
    


