#!/usr/bin/env python
# -*- coding: utf-8 -*-

#检测李老师给我的POI文件里的点与我自己获取的武汉POI里面的点的差异
old_poi_id_list = []
f = open("txt/list/old_pois.txt", "r")
for line in f:
    old_poi_id_list.append(line[:-1])
f.close()
print u"old_pois.txt读取完毕"
    
new_poi_id_list = []
f = open("txt/list/new_pois.txt", "r")
for line in f:
    new_poi_id_list.append(line[:-1])
f.close()
print u"new_pois.txt读取完毕"

f = open("txt/poi_difference.txt", "a")
print u"正在查询，请等待"
for old_poi_id in old_poi_id_list:
    if old_poi_id not in new_poi_id_list:
        f.write(old_poi_id+"\n")
        
f.flush()
f.close()
