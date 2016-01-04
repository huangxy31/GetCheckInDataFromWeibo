#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8

from weibo import APIClient
import webbrowser#python内置的包
import urllib2
from pinyin import PinYin
import sys
import time



APP_KEY = '1163934014'
APP_SECRET = '3830048e5d6087700e68b787c2e83c3c'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
access_token = "2.00MIE22GQ6klQBdfe7497f230yWjCW" # 新浪返回的token，类似abc123xyz456

#利用官方微博SDK
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
#得到授权页面的url，利用webbrowser打开这个url
url = client.get_authorize_url()

#access_token = "2.00MIE22GQ6klQBdfe7497f230yWjCW" # 新浪返回的token，类似abc123xyz456
#print access_token
expires_in = 1609052638
# 设置得到的access_token
client.set_access_token(access_token, expires_in)

#接下来就可以调用api了
my_keyword = raw_input(u"请输入地名：")
my_keyword = my_keyword.decode('gbk').encode('utf-8')

#getPOIs(my_keyword)

#汉字转拼音
def hanziToPinyin(hanzi):
    test = PinYin()
    test.load_word()
    return test.hanzi2pinyin_split(string=hanzi, split="_")

#获取POI
def getPOIs(my_keyword):
    r = client.place.pois.search.get(keyword=my_keyword)
    type = sys.getfilesystemencoding()#去掉乱码
    #print r
    if "pois" in r:
        total_number = r.total_number#总个数
        count = 50#一页的个数
        print u"总共"+str(total_number)+u"个POI"
        page_number = 1
        #计算页数
        if(total_number%50>0):
            page_number = total_number/count + 1
        else:
            page_number = total_number/count

        #创建txt
        current_time = time.strftime("%m%d%H%M%S",time.localtime(time.time()))
        #file_name = hanziToPinyin(my_keyword) + str(current_time) + ".txt"
        file_name = "data/"+ hanziToPinyin(my_keyword) + ".txt"
        poi_file=open(file_name,"a")

        #循环每一页
        poi_index = 1
        start_page = raw_input(u"请输入起始页数：")
        for page_index in range(int(start_page), page_number+1):
            r = client.place.pois.search.get(keyword=my_keyword, count=50, page=page_index)#调用新浪API
            if "pois" not in r:
                print u"完成！"
                break
            poi_index = (page_index-1) * count + 1
            print u"开始获取第"+str(page_index)+u"页数据"
            for st in r.pois:
                poi_info = []

                poi_info.append(str(poi_index))
                poi_info.append(str(st.poiid))
                poi_info.append(str(st.title))
                poi_info.append(str(st.address))
                poi_info.append(str(st.lon))
                poi_info.append(str(st.lat))
                poi_info.append(str(st.category))
                poi_info.append(str(st.city))
                poi_info.append(str(st.province))
                poi_info.append(str(st.categorys))
                poi_info.append(str(st.category_name))
                if "id" in st.district_info:
                    poi_info.append(str(st.district_info.id))
                else:
                    poi_info.append("")
                    
                if "title" in st.district_info:
                    poi_info.append(str(st.district_info.title))
                else:
                    poi_info.append("")

                if "county" in st.district_info:
                    poi_info.append(str(st.district_info.county))
                else:
                    poi_info.append("")

                poi_info.append(str(st.checkin_user_num))
                poi_info.append(str(st.checkin_num))
                poi_info.append(str(st.photo_num))
                poi_info.append(str(st.dianping_num))
                
                #print poi_info
                #print ",".join(poi_info)
                poi_text =  ",".join(poi_info) + "\n"
                poi_file.write(poi_text)
                poi_index += 1
            print "完成第"+str(page_index)+"页，还剩"+str(page_number-page_index)+"页"

        #关闭文件夹
        poi_file.flush()
        poi_file.close()
    

getPOIs(my_keyword)
"""
rint client.statuses__public_timeline()
statuses = client.statuses__public_timeline()['statuses']
length = len(statuses)
#输出了部分信息
for i in range(0,length):
	print u'昵称：'+statuses[i]['user']['screen_name']
	print u'简介：'+statuses[i]['user']['description']
	print u'位置：'+statuses[i]['user']['location']
	print u'微博：'+statuses[i]['text']
"""
