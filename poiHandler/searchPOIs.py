#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################
#读取all_poi_with_address.txt，通过关键字查找poi
#############################################################

poi_list = []
f = open("txt/all_poi_with_address.txt", "r")

for line in f:
    poi_info = line.split()
    poi_list.append(poi_info)    
f.close()

def seach_poi_by_keyword(keyword):
    poi_count = 0
    for poi in poi_list:
        poi_name = poi[2]
        poi_address = poi[3]

        if keyword in poi_name or keyword in poi_address:
            poi_count += 1
            
    return poi_count

keyword = raw_input(u'请输入关键字(输入0退出程序)：')

while keyword != '0':
    count = seach_poi_by_keyword(keyword)
    print keyword.decode('gbk').encode('utf-8')+u'共'+ str(count) + u'个POI'
    keyword = raw_input(u'请输入关键字(输入0退出程序)：')
