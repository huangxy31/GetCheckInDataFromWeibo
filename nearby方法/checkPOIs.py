#!/usr/bin/env python
# -*- coding: utf-8 -*-

#用于检查数据获取是否完整


def get_list_index(poi_index):
        for i in range(len(poi_list)):
                if poi_index == poi_list[i]:
                        return i
        print u"POI编号不存在于列表中，请重新输入"
        return -1

#############################################################
#读取单个POI文件，返回POI个数
#############################################################
def get_file_poi_num(poi_index):
    file_name = "pois/" + str(poi_index) + ".txt"
    poi_file = open(file_name, "r")
    count = 0
    for line in poi_file:
        count += 1
    poi_file.close()
    return count

#############################################################
#读取wuhan_poi.txt，保存数据
#############################################################
poi_list = []
f = open("wuhan_poi.txt", "r")
for line in f:
    poi_list.append(line.split())
f.close()

#############################################################
#在searchAgain.txt中记录需要重新检索的POI
#############################################################
search_again_file=open("searchAgain.txt","a")
for poi in poi_list:
    poi_index = int(poi[0])
    list_poi_num = int(poi[1])
    if list_poi_num > 0:
        file_poi_num = get_file_poi_num(poi_index)
        if abs(list_poi_num - file_poi_num) > 10:
            poi_info = []
            poi_info.append(str(poi_index))#poi编号
            poi_info.append(str(list_poi_num))#记录的点数
            poi_info.append(str(file_poi_num))#单独文件中的点数
            text = ",".join(poi_info) + "\n"
            search_again_file.write(text)
            print ",".join(poi_info)

search_again_file.flush()
search_again_file.close()        
