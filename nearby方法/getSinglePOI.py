#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import myWeibo
import sys

sys.setrecursionlimit(1000000)

lat_min = 29.97480450855934
lon_min = 113.70023055784257
lat_max = 31.35129983240219
lon_max = 115.07973947933637
#dLat = 62000
#dLon = 153000

poi_range_origin = 2500#POI范围

#将区域以lat_step*lon_step的大小划分网格
#lat_step = (lat_max - lat_min) / (dLat/poi_range)
#lon_step = (lon_max - lon_min) / (dLon/poi_range)

lat_step_origin = 0.03#步长
lon_step_origin = 0.03#步长

total_lat_num = int(math.ceil((lat_max - lat_min )/lat_step_origin))#循环次数
total_lon_num = int(math.ceil((lon_max - lon_min )/lon_step_origin))
print total_lat_num * total_lon_num
#print lat_step, lon_step
#############################################################
#读取excep.txt文件部分
#############################################################
poi_list = []
f = open("except.txt", "r")
for line in f:
    poi_list.append(int(line))
f.close() 

def get_list_index(poi_index):
        for i in range(len(poi_list)):
                if poi_index == poi_list[i]:
                        return i
        print u"POI编号不存在于列表中，请重新输入"
        return -1
#############################################################
#微博部分
#############################################################

#985, 170
#############################################################
#微博部分
#############################################################
my_key = '1163934014'
my_secret = '3830048e5d6087700e68b787c2e83c3c'
my_access_token = "2.00MIE22GQ6klQBdfe7497f230yWjCW"
#my_access_token = "2.00MIE22G0jbkXNbd85efbb1700IwBq"
#my_access_token = "2.00sXyT2GGjwv4Ef26967559c0oVlFM"
#my_access_token = "2.00PWey2Gi3oYcEbfac9bd2d9acLwcC"
#my_access_token = "2.00cwey2G28HqADd499e1cddd0NVRm2"
#my_access_token = "2.002nOx2GJGGgGEaa5e600f73DmepBE"
#my_access_token = "2.00jh8z2GpBdiwD6f08cce3ac0CXq55"

#my_access_token = "2.00sXyT2GQ6klQBeba1a5ce33EhSiDD"

my_client = myWeibo.set_weibo(my_key, my_secret, my_access_token)

"""
my_keyword = "广埠屯"
r = my_client.place.pois.search.get(keyword=my_keyword, count=2, page=1)#调用新浪API
r = my_client.place.nearby.pois.get(lat=30.52420957, long=114.36054116, range=poi_range_origin)
print r
"""

#############################################################
#算法部分
#############################################################
def get_total_poi_num(lon, lat, poi_range):
        global api_count
        #调用新浪API，每页50个，按距离由近到远排序
        r = my_client.place.nearby.pois.get(lat=lat, long=lon, range=poi_range_origin, count=50, sort=1)
        api_count += 1
        if "total_number" not in r:
                return 0
        else:
                return r.total_number

        

#根据点数计算每页最合适的显示个数，最后一页（API不能获取到）点数小于10
def get_count(num):
        if num < 50:
                return num
        for i in range(31):
                if 0 < num % (50 - i) < 10:
                        print (50 - i)
                        return (50 - i)
        return 30



#获取单个POI搜索的详细信息列表
def get_POI_info(lon, lat, page):
    r = my_client.place.nearby.pois.get(lat=lat, long=lon, range=poi_range_origin, count=50, sort=1)
    if "pois" not in r:
        total_number = 0
        print u"查询不到POI！"
        
    else:
        #创建单个POI搜索详细结果文件
        info_file_name = "pois/single/" + str(cur_poi_index)+ ".txt"
        poi_info_file=open(info_file_name,"a")
        
        total_number = r.total_number#总个数
        page_count = get_count(total_number)#一页的个数
        print page_count
        #print u"总共"+str(total_number)+u"个POI"
        page_number = 1
        #计算页数
        if(total_number%page_count>0):
            page_number = total_number/page_count + 1
        else:
            page_number = total_number/page_count


        print "POI:"+str(cur_poi_index), "lon:"+str(lon), "lat:"+str(lat), "total_number:"+str(total_number)

        #循环每一页
        poi_index = 1
        #start_page = raw_input(u"请输入起始页数：")
        #start_page = 1
        for page_index in range(int(page), page_number+1):
            r = my_client.place.nearby.pois.get(lat=lat, long=lon, range=poi_range_origin, count=page_count, sort=1, page=page_index)
            if "pois" not in r:
                print "POI:"+str(cur_poi_index)+u"完成！\n"
                break
            poi_index = (page_index-1) * page_count + 1
            #print u"开始获取第"+str(page_index)+u"页数据"
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
                poi_info.append(str(st.distance))
                
                #print poi_info
                #print ",".join(poi_info)
                poi_text =  ",".join(poi_info) + "\n"
                poi_info_file.write(poi_text)
                poi_index += 1
            print "POI:"+str(cur_poi_index)+u"完成第"+str(page_index)+u"页，还剩"+str(page_number-page_index)+u"页"
        poi_info_file.flush()
        poi_info_file.close()

#cur_poi_index = 0

def loop_search_poi():
        flag = True#控制循环
        while flag:
                global cur_poi_index
                cur_poi_index = int(raw_input(u'请输入POI编号(输入0退出)：'))
                if cur_poi_index == 0:
                        return
                
                while cur_poi_index>= total_lat_num * total_lon_num or cur_poi_index<0:
                        print u"超出范围，请输入0-"+str(total_lat_num * total_lon_num)+"之间的数字！"
                        cur_poi_index = int(raw_input(u'请输入POI编号：'))

                start_lon = lon_min + cur_poi_index % total_lon_num * lon_step_origin
                start_lat = lat_min + cur_poi_index / total_lat_num  * lat_step_origin
                #print "lon:"+str(start_lon), "lat:"+str(start_lat)

                start_page = raw_input(u"请输入起始页数：")
                get_POI_info(start_lon, start_lat, start_page)


def get_remain_pois():
        global cur_poi_index
        cur_poi_index = int(raw_input(u'请输入POI编号(输入0退出)：'))
        if cur_poi_index == 0:
                return

        while cur_poi_index>= total_lat_num * total_lon_num or cur_poi_index<0:
                print u"超出范围，请输入0-"+str(total_lat_num * total_lon_num)+"之间的数字！"
                cur_poi_index = int(raw_input(u'请输入POI编号：'))

        list_index = get_list_index(cur_poi_index)
        while list_index == -1:
                cur_poi_index = int(raw_input(u'请输入POI编号：'))
                list_index = get_list_index(cur_poi_index)

        start_lon = lon_min + cur_poi_index % total_lon_num * lon_step_origin
        start_lat = lat_min + cur_poi_index / total_lat_num  * lat_step_origin

        start_page = raw_input(u"请输入起始页数：")
        get_POI_info(start_lon, start_lat, start_page)

                #循环剩余的POI
        for i in range(list_index+1, len(poi_list)):
                cur_poi_index = poi_list[i]
                cur_lon = lon_min + cur_poi_index % total_lon_num * lon_step_origin
                cur_lat = lat_min + cur_poi_index / total_lat_num  * lat_step_origin
                get_POI_info(cur_lon, cur_lat, 1)

loop_search_poi()

#get_remain_pois()
    

#############################################################
#获取单个POI
#############################################################
"""
cur_poi_index = int(raw_input(u'请输入POI编号：'))
while cur_poi_index>= total_lat_num * total_lon_num or cur_poi_index<0:
        print u"超出范围，请输入0-"+str(total_lat_num * total_lon_num)+"之间的数字！"
        cur_poi_index = int(raw_input(u'请输入POI编号：'))

start_lon = lon_min + cur_poi_index % total_lon_num * lon_step_origin
start_lat = lat_min + cur_poi_index / total_lat_num  * lat_step_origin
print "lon:"+str(start_lon), "lat:"+str(start_lat)

start_page = raw_input(u"请输入起始页数：")
get_POI_info(start_lon, start_lat, start_page)
"""

