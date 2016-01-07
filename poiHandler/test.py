#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################
#读取all_poi_new.txt，保存数据
#############################################################
poi_id_list = []
f = open("txt/all_poi_new.txt", "r")

for line in f:
    poi_info = line.split()
    poi_id = poi_info[1]
    poi_id_list.append(poi_id)
    
f.close()

