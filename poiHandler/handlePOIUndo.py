#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import libs.myWeibo


#处理数据有问题的点

#获取需要处理的POI列表
poi_list = []
f = open("txt/poi_undo3.txt", "r")
for line in f:
    poi_list.append(line.split())
f.close()


def get_list_index_by_id(poiid):
    for i in range(len(poi_list)):
        poi = poi_list[i]
        if poiid == poi[3]:
            return i
    return -1
#############################################################
#微博部分
#############################################################
acess_token_index = 3
app_info_index = 0

#开始调用微博
my_client = libs.myWeibo.get_client(app_info_index, acess_token_index)

#处理错误情况
while my_client == -1:
    print u"acess_token_index与app_info_index错误请重新输入！"
    acess_token_index = int(raw_input(u"acess_token_index:"))
    app_info_index = int(raw_input(u"app_info_index:"))
    my_client = libs.myWeibo.get_client(app_info_index, acess_token_index)

#############################################################
#调用微博api，获取某一poiid的POI信息
#############################################################
#在poi_update.txt中记录新的POI信息
poi_update_file = open("txt/poi_update2.txt", "a")

def write_poi_info(poi_index, page, page_index, poi_id):
    #获取poi信息
    r = my_client.place.pois.show.get(poiid=poi_id)
    if "poiid" in r:
        poi_info = []

        poi_info.append(str(poi_index))
        poi_info.append(str(page))
        poi_info.append(str(page_index))
        poi_info.append(str(r.poiid))
        poi_info.append(str(r.title))
        poi_info.append(str(r.address))
        poi_info.append(str(r.lon))
        poi_info.append(str(r.lat))
        poi_info.append(str(r.category))
        poi_info.append(str(r.city))
        poi_info.append(str(r.province))
        poi_info.append(str(r.categorys))
        poi_info.append(str(r.category_name))
        if "id" in r.district_info:
            poi_info.append(str(r.district_info.id))
        else:
            poi_info.append("")
            
        if "title" in r.district_info:
            poi_info.append(str(r.district_info.title))
        else:
            poi_info.append("")

        if "county" in r.district_info:
            poi_info.append(str(r.district_info.county))
        else:
            poi_info.append("")

        poi_info.append(str(r.checkin_user_num))
        poi_info.append(str(r.checkin_num))
        poi_info.append(str(r.photo_num))
        #poi_info.append(str(r.dianping_num))
        poi_info.append(str(r.tip_num))
        #poi_info.append(str(r.distance))
        text = "\t".join(poi_info) + "\n"
        poi_update_file.write(text)        
    else:
        print u"POI:"+str(poi_id)+u"不存在！"


#############################################################
#开始获取
#############################################################
#start_id = raw_input(u"请输入起始点POIID:")
#start_index = get_list_index_by_id(start_id)

start_index = int(raw_input(u"请输入循环开始位置(i):"))

for i in range(start_index, len(poi_list)):
    poi = poi_list[i]
    poi_index = poi[0]
    page = poi[1]
    page_index = poi[2]
    poi_id = poi[3]
    write_poi_info(poi_index, page, page_index, poi_id)
    print u"POI:"+str(poi_id)+"完成，i="+str(i)



poi_update_file.flush()
poi_update_file.close()
