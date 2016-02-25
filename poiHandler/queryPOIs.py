#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################
#读取wuhan_weibo_poi.txt，通过关键字查找poi，并生成txt
#############################################################

import os

poi_list = []
f = open("txt/wuhan_weibo_poi.txt", "r")

#读取每一行的poi信息
for line in f:
    #分割为数组
    poi_info = line.split()
    poi_list.append(poi_info)    
f.close()

def seach_poi_by_keyword(keyword):
    poi_count = 0 #POI数
    file_path = 'txt/queryResults/'+keyword+".txt"#保存为txt
    #判断文件是否存在
    if os.path.exists(file_path):
        print u'文件已存在'
        return '?'

    else:
        #创建文件
        f = open(file_path,"a")        
        #循环POI
        for poi in poi_list:
            poi_name = poi[4]#POI名
            poi_address = poi[5]#POI地址

            if keyword in poi_name or keyword in poi_address:
                poi_count += 1
                f.write('\t'.join(poi[3:])+"\n")
                #print poi
        f.flush()
        f.close()
    return poi_count

keyword = raw_input(u'请输入关键字(输入0退出程序)：')

while keyword != '0':
    count = seach_poi_by_keyword(keyword)
    print keyword.decode('gbk').encode('utf-8')+u'共'+ str(count) + u'个POI'
    keyword = raw_input(u'请输入关键字(输入0退出程序)：')
