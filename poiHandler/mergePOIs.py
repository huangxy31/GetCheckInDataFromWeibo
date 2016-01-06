#!/usr/bin/env python
# -*- coding: utf-8 -*-

#读取所有POI文件，将其合并到一个文件里，删除掉重复的点
all_poi_file=open("all_poi_new.txt","a")
poi_id_list = []
cur_poi_index = 1

def get_list_index(poi_index):
        for i in range(len(poi_list)):
                if poi_index == poi_list[i]:
                        return i
        print u"POI编号不存在于列表中，请重新输入"
        return -1

#############################################################
#读取单个POI文件，写入all_poi.txt
#############################################################
def write_poi_info(poi_index):
    global cur_poi_index
    file_name = "pois/" + str(poi_index) + ".txt"
    poi_file = open(file_name, "r")
    for line in poi_file:
        #获取POI编号
        poi_id = line.split(",")[1]
        #判断编号是否存在于列表中
        if poi_id not in poi_id_list:
                poi_id_list.append(poi_id)
                #写入文件
                text = str(cur_poi_index) +","+ str(poi_index)+","+ line
                all_poi_file.write(text)
                cur_poi_index += 1
    print u"POI:"+str(poi_index)+u"完成"
    poi_file.close()

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

for poi in poi_list:
    poi_index = int(poi[0])
    list_poi_num = int(poi[1])
    if list_poi_num > 0:
        write_poi_info(poi_index)


"""        
        if abs(list_poi_num - file_poi_num) > 10:
            poi_info = []
            poi_info.append(str(poi_index))#poi编号
            poi_info.append(str(list_poi_num))#记录的点数
            poi_info.append(str(file_poi_num))#单独文件中的点数
            text = ",".join(poi_info) + "\n"
            all_poi_file.write(text)
            print ",".join(poi_info)
"""

all_poi_file.flush()
all_poi_file.close()        
