import requests
import re
import time
import pandas as pd

#以 家电类商品 为例
keyword = "家电"
key = ['冰箱','洗衣机','电视','扫地机器人','微波炉','电水壶','破壁机','电饭煲','电热水器','空调']

# 设置请求头
headers = {
	'User-Agent':'Mozilla/5.0',
	'Cookie': 'miid=748525271215462194; cna=axamFa4NczsCAWdVkNpE8ape; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; xlly_s=1; _samesite_flag_=true; cookie2=1bc5181533035cd58b99a0447e8f6100; t=aab17e0bc1aaee3ecae9a75596652ecf; _tb_token_=5ff76b876bbd; sgcookie=E100ugvzehgmqYYo7OCkS7b9ogqvWdvuv7NSeClG0lNSPiKccts4Qbn5APss5GY8k6Co4UxtHymTQx5%2FiIlXwQrjBg%3D%3D; unb=2613464230; uc3=id2=UU6gYugIoRCjHg%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dCuwJEbvObnoiNkx8%3D&nk2=q5ZgCQhjeD3rI0jR; csg=5300db07; lgc=%5Cu8BA4%5Cu771F%5Cu6267%5Cu7740%5Cu8BB8%5Cu613F; cancelledSubSites=empty; cookie17=UU6gYugIoRCjHg%3D%3D; dnk=%5Cu8BA4%5Cu771F%5Cu6267%5Cu7740%5Cu8BB8%5Cu613F; skt=9836294b4f6cb70c; existShop=MTYyNjQyMTU4NA%3D%3D; uc4=nk4=0%40qSNLQxMR8jy2UO%2BMVFbxF%2F9Y9QVd9kg%3D&id4=0%40U2xt%2BjdkaOMgXbi%2BKiURX5nNcO2x; tracknick=%5Cu8BA4%5Cu771F%5Cu6267%5Cu7740%5Cu8BB8%5Cu613F; _cc_=VT5L2FSpdA%3D%3D; _l_g_=Ug%3D%3D; sg=%E6%84%BF01; _nk_=%5Cu8BA4%5Cu771F%5Cu6267%5Cu7740%5Cu8BB8%5Cu613F; cookie1=BxNYKYLA2oI9n7fyr3kkwZETMJ3KEvK9kUWwjSyJNws%3D; enc=eYQdK%2BXl%2BARo4vjEKKRSw%2FTRUph1yo%2FBbKC0uAu%2Bt86N2oTU2uVKiFmipzRG881sv5y4isU59u85qMRt3BKc9g%3D%3D; _uab_collina=162642158555125863154919; alitrackid=login.taobao.com; lastalitrackid=login.taobao.com; mt=ci=4_1; x5sec=7b227365617263686170703b32223a226534623861353566353337646331396162376565633936646238393735353236434962367849634745496e6d2f6448503273447046786f4d4d6a59784d7a51324e44497a4d4473794d4b6546677037382f2f2f2f2f77453d227d; JSESSIONID=ED57FA74CE957627464AB6EAAC8C05A9; tfstk=ciwdBNGpHNbht4oT0WCGNSFKWtjcZstKrHgJeM8zzmOCyl9Ri_e0HS2AO0oR-GC..; l=eB_fpFr4jtH9sjyBBOfZlurza77TAIRAguPzaNbMiOCP_V5H5ZNcW6TXt_LMCnGVh6m2R3kRsBPaBeYBqCj0JeHw2j-laMMmn; isg=BJmZtpMiHfnZw8FtH0wlTuqYqIVzJo3YHoUcRbtOPkA_wrlUA3dyqAfYxIa0-iUQ; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie14=Uoe2yztIOUjGYQ%3D%3D&existShop=false&cookie21=UtASsssmeW6lpyd%2BBROh&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0'
	}
name = []
link_id = []
frm = []
for i in key:
	# 获取搜索页面
	url = 'https://s.taobao.com/search?q='+i
	res = requests.get(url = url,headers = headers)
	# 筛选数据
	reg = '"nid":"(\d{1,19})".*?,"title":"(.*?)"'
	ans = re.findall(reg,res.content.decode('utf-8'))
	# 写入数据
	for j in ans:
		name.append(j[1])
		link_id.append(j[0])
		frm.append(i)
	time.sleep(3)

gd_detail = {"商品属性":frm,"商品名称":name,"商品id":link_id}
result = pd.DataFrame(gd_detail)
result.to_excel('GoodsInf.xlsx')
