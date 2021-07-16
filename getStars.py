import requests
from lxml import etree
import time
import re
import pandas as pd

# 设置请求头
headers = {
	'User-Agent':'Mozilla/5.0',
    'Cookie':'miid=748525271215462194; cna=axamFa4NczsCAWdVkNpE8ape; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; xlly_s=1; t=aab17e0bc1aaee3ecae9a75596652ecf; lgc=%5Cu8BA4%5Cu771F%5Cu6267%5Cu7740%5Cu8BB8%5Cu613F; tracknick=%5Cu8BA4%5Cu771F%5Cu6267%5Cu7740%5Cu8BB8%5Cu613F; enc=eYQdK%2BXl%2BARo4vjEKKRSw%2FTRUph1yo%2FBbKC0uAu%2Bt86N2oTU2uVKiFmipzRG881sv5y4isU59u85qMRt3BKc9g%3D%3D; mt=ci=4_1; _m_h5_tk=58960e32e5ccee849aee9eea8374a77b_1626459369931; _m_h5_tk_enc=af1b24a89d9e5ca8218653c01dd3d68f; sgcookie=E100xbFciGnpq7UXOA604n%2FTFw8ba4WyPdtp10bYlHJDbTCZNOTYxn5%2FVaUE1tvpoFR9AU8k1qxZYZqMJXLZieCM0g%3D%3D; uc3=lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dCuwJEa6UeNqyWfmI%3D&id2=UU6gYugIoRCjHg%3D%3D&nk2=q5ZgCQhjeD3rI0jR; uc4=id4=0%40U2xt%2BjdkaOMgXbi%2BKiURX55HFdhY&nk4=0%40qSNLQxMR8jy2UO%2BMVFbxF%2F9Y8kYXLbw%3D; _cc_=W5iHLLyFfA%3D%3D; uc1=cookie14=Uoe2yztP919T8A%3D%3D; _tb_token_=3b0ebdbb5ee11; cookie2=16bd8cf3b34be2397b6712b5d866f1e9; v=0; isg=BNzcaiXg0B4D-aRCUn84iR8brfqOVYB_a2Y5arbdp0eNAX2L3mWbDlu4ZWn5sbjX; l=eB_fpFr4jtH9sL5KBOfZourza77OxIRbiuPzaNbMiOCPOvCpR8clW6TbM9T9CnGVn6l9R3kRsBPwB4LLxy4egxv9-eTCgsDKndLh.; tfstk=ciMNBdNXsdpa0r2XwRwVczbaaFeOZUa0P9rzsX6gVjGNUSVGiQQYxhcuYo7KJ5f..'
}
requests.adapters.DEFAULT_RETRIES = 5

# 读取excel获取商品ID
df = pd.read_excel('GoodsInf.xlsx',engine='openpyxl')

# 初始化表单
disc = []
ser = []
liu = []

for j in range(0,len(df)):
    
    url = f"https://detail.tmall.com/item.htm?id={str(df['商品id'][j])}"

    # 发起get请求
    try:
        res = requests.get(url=url,headers=headers)
    except:
        disc.append(0)
        ser.append(0)
        liu.append(0)
        continue
    else:
        if res.status_code == 200 :
            print('第'+str(j)+'件商品 商店评分爬取中……')
            html = etree.HTML(res.text)
            # 规格化数据
            ans = html.xpath('//span[@class="shopdsr-score-con"]/text()')
            # print(ans)
            if not ans:
                shopid = re.findall("id          : '(\d{5,15})',[\s\S]*?id  : '(\d{5,15})',",res.text)
                if not shopid:
                    disc.append(0)
                    ser.append(0)
                    liu.append(0)
                    continue
                tmp = requests.get(url=f"https://hdc1new.taobao.com/asyn.htm?userId={shopid[0][0]}&shopId={shopid[0][1]}",headers=headers)
                ans = re.findall("<em>(\d\.\d)</em>",tmp.text)
                if not ans:
                    disc.append(0)
                    ser.append(0)
                    liu.append(0)
                    continue
            disc.append(ans[0])
            ser.append(ans[1])
            liu.append(ans[2])
        else:
            print('错误：',res.status_code)

        # 停留1s
        time.sleep(0.2)

# 写入excel
ndf = {}
ndf['商店描述'] = disc
ndf['商店服务'] = ser
ndf['商店物流'] = liu
df = pd.concat([df,pd.DataFrame(ndf)],axis=1)
df.to_excel('GoodsInf.xlsx')


