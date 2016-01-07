#!/usr/bin/env python
# -*- coding:utf-8 -*-

from weibo import APIClient
import webbrowser#python内置的包
import urllib2

def set_weibo(appKey, appSecret, accessToken):
    APP_KEY = appKey
    APP_SECRET = appSecret
    CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
    access_token = accessToken # 新浪返回的token，类似abc123xyz456

    #利用官方微博SDK
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    #得到授权页面的url，利用webbrowser打开这个url
    url = client.get_authorize_url()

    #access_token = "2.00MIE22GQ6klQBdfe7497f230yWjCW" # 新浪返回的token，类似abc123xyz456
    #print access_token
    expires_in = 1609052638
    # 设置得到的access_token
    client.set_access_token(access_token, expires_in)
    #r = client.place.pois.search.get(keyword=my_keyword, count=50, page=1)#调用新浪API
    #print r
    return client

def get_client(app_info_index, acess_token_index):
    #读取appKey和appSecret
    app_info_list = []
    f = open("../libs/appKey.txt", "r")
    for line in f:
        app_info_list.append(line[:-1].split(","))
    f.close()

    #读取accessToken
    access_token_list = []
    f = open("../libs/accessToken.txt", "r")
    for line in f:
        access_token_list.append(line[:-1])
    f.close()

    #参数不正确的话返回-1
    if app_info_index>=len(app_info_list) or acess_token_index>=len(access_token_list):
        return -1
    
    my_key = app_info_list[app_info_index][0]
    my_secret = app_info_list[app_info_index][1]
    my_access_token = access_token_list[acess_token_index]
    print my_key, my_secret, my_access_token

    #开始调用微博
    my_client = set_weibo(my_key, my_secret, my_access_token)
    return my_client

#get_client(0, 0)
