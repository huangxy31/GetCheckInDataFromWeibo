#!/usr/bin/env python
# -*- coding: utf-8 -*-

#获取签到数据

import sys
sys.path.append("..")
import libs.myWeibo
import math
from libs.weibo import APIError
import traceback
from ssl import SSLError
import time



#获取POI列表
poi_list = []
f = open("txt/check_in_list.txt", "r")
for line in f:
    poi_list.append(line[:-1])
f.close()


def get_list_index_by_id(poiid):
    for i in range(len(poi_list)):
        poi = poi_list[i]
        if poiid == poi:
            return i
    return -1


#############################################################
#微博部分
#index:21378 page:1
#############################################################
acess_token_index = 1
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
#获取当前系统时间
#############################################################
def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

#############################################################
#调用微博api，获取某一POI的签到信息
#############################################################
cur_check_in_index = 1
#在check_in_file中写入签到信息
def write_check_in_data(r, check_in_file):
    global cur_check_in_index
    if "statuses" in r:
        for status in r.statuses:
            check_in_info = []
            check_in_info.append(str(cur_check_in_index))
            check_in_info.append(str(status.created_at))#创建时间
            check_in_info.append(str(status.id))#ID
            if "user" in status:
                check_in_info.append(str(status.user.id))#用户ID
                check_in_info.append(str(status.user.gender))#用户性别
            else:
                #若微博已删除则无用户信息
                check_in_info.append("")
                check_in_info.append("")
            if "state" in status:
                #微博状态，5为删除，0为普通
                check_in_info.append(str(status.state))
            else:
                check_in_info.append("0")
            
            text = "\t".join(check_in_info) + "\n"
            check_in_file.write(text)
            cur_check_in_index += 1

#记录错误日志
def write_error_log(error):
    f=open("txt/log.txt",'a')
    f.write(get_current_time() + '\n') #记录时间
    f.write(str(error) + '\n') #记录错误
    f.flush()  
    f.close()
    print u'写入日志'
    
#处理API错误
def api_error_handle(error, poi_index, poi_id, page):
    if '10023' not in str(error):
    #日志记录
        write_error_log(error)
        
    #'10023'表示User requests out of rate limit!
    #'23201'表示Backend Service Connect Timeout!
    #'10006'表示access token无效
    if '10023' in str(error) or '23201' in str(error) or '10006' in str(error):
        if '10006' in str(error):
            print u'Access Token无效'
        print u"index:"+str(poi_index), u"page:"+str(page), u"API调用出错"
        return page
    #'23805'表示不存在这个POI!
    elif '23805' in str(error):
        #没有签到数据就返回
        print u"POI:"+str(poi_index)+u", POIID:"+str(poi_id)+u"没有签到数据"
        return -2
    else:
        print error
        print u"POI:"+str(poi_index)+u", POIID:"+str(poi_id)+u"出错"
        sys.exit()

#处理SSL timed out错误
def ssl_error_handle(error, poi_index, poi_id, page):
    #time out处理
    #日志记录
    write_error_log(error)
    if 'timed out' in str(error):
        print u"index:"+str(poi_index), u"page:"+str(page), u"超时重试！"
        return page
    else:
        print error
        print u"POI:"+str(poi_index)+u", POIID:"+str(poi_id)+u"出错"
        sys.exit()

           
#从某页起，获取poi_id的签到信息
def write_poi_info(poi_index, poi_id, start_page):
    #获取poi信息
    count = 50
    try:
        r = my_client.place.poi_timeline.get(poiid=poi_id, count=count, page=1)
        #print poi_id, count, "?"
        if "statuses" not in r:
            #没有签到数据就返回
            msg = u"POI:"+str(poi_index)+u", POIID:"+str(poi_id)+u"没有签到数据"
            print msg
            write_error_log(msg)
            return -2
        else:
            #创建文件
            file_name = poi_id[:8] + "/" + poi_id + ".txt"
            check_in_file = open("check in/"+file_name, "a")
            global cur_check_in_index
            cur_check_in_index = (start_page - 1) * count + 1

            #计算页数,大于2则循环
            total_number = int(r.total_number)
            print total_number
            page_count = int(math.ceil(float(total_number) / float(count)))
            #print start_page, page_count+1
            
            #写入第一页数据
            if(start_page == 1):
                write_check_in_data(r, check_in_file)
                start_page += 1
                print u"POI:"+str(poi_index)+u", POIID:"+str(poi_id)+u" 第1页完成"
                   
            for i in range(start_page, page_count+1):
                try:
                    r = my_client.place.poi_timeline.get(poiid=poi_id, count=count, page=i)
                    #print poi_id, count, i
                    write_check_in_data(r, check_in_file)
                    print u"POI:"+str(poi_index)+u", POIID:"+str(poi_id)+u" 第"+str(i)+u"页完成"
                #处理错误情况
                except APIError, e:
                    return api_error_handle(e, poi_index, poi_id, i)                        
                #time out处理
                except SSLError, e:
                    return ssl_error_handle(e, poi_index, poi_id, i)

                
            print u"POI:"+str(poi_index)+u", POIID:"+str(poi_id)+u"完成"
            check_in_file.flush()
            check_in_file.close()
            return -1

  
    except APIError, e:
        return api_error_handle(e, poi_index, poi_id, start_page)            
    #time out处理
    except SSLError, e:
        return ssl_error_handle(e, poi_index, poi_id, start_page)
            
        


#############################################################
#开始获取
#############################################################
"""
poi = poi_list[1]
poi_index = poi[0]
poi_id = poi[1]
write_poi_info(poi_index, poi_id, 1)

for i in range(start_index, len(poi_list)):
    poi_id = poi_list[i]
    if i == start_index:
        break_page = write_poi_info(i, poi_id, start_page)
    else:
        break_page = write_poi_info(i, poi_id, 1)
        print break_page
        if break_page != -1:
            break
"""

start_index = int(raw_input(u"请输入循环开始位置(i):"))
start_page = int(raw_input(u"请输入签到查询起始页码:"))

poi_not_find_list = []

#从start_index和start_page开始，循环获取签到数据
def new_start_run():
    for i in range(start_index, len(poi_list)):
        poi_id = poi_list[i]
        if i == start_index:
            break_page = write_poi_info(i, poi_id, start_page)
            if break_page > 0:
                #中断返回中断时的index和page
                return i, break_page
            #完成这一页
            elif break_page == -1:
                continue
            else:
                poi_not_find_list.append(str(i)+","+str(poi_id))
                continue
        else:
            break_page = write_poi_info(i, poi_id, 1)
            #print break_page
            #API错误，退出
            if break_page > 0:
                #中断返回中断时的index和page
                return i, break_page
            #完成这一页
            elif break_page == -1:
                continue
            else:
                poi_not_find_list.append(str(i)+","+str(poi_id))
                continue
    #全部完成返回-1，-1
    return -1, -1

new_index, new_page = new_start_run()

def loop_run():
    global new_index, new_page, start_index, start_page, my_client
    #循环完成
    if new_index == -1 and new_page=-1:
        sys.exit()
    if new_index != -1:
        for i in range(22):
            acess_token_index = i
            app_info_index = 0
            #开始调用微博
            my_client = libs.myWeibo.get_client(app_info_index, acess_token_index)
            start_index = new_index
            start_page = new_page
            new_index, new_page = new_start_run()


#############################################################
#一切为了循环
#############################################################

import libs.timeHandler
loop_run()
libs.timeHandler.runTask(loop_run, min=30)


