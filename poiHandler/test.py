#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################
#读取wuhan_poi.txt，保存数据
#############################################################
poi_list = []
f = open("txt/all_poi_new.txt", "r")
count = 0
for line in f:
    count += 1
f.close()
print count
