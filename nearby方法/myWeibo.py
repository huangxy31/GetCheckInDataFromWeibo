#!/usr/bin/env python
# -*- coding:utf-8 -*-

from weibo import APIClient
import webbrowser#python内置的包
import urllib2

def set_weibo(appKey, appSecret, accessToken):
    """
    APP_KEY = '1163934014'
    APP_SECRET = '3830048e5d6087700e68b787c2e83c3c'
    CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
    access_token = "2.00MIE22GQ6klQBdfe7497f230yWjCW" # 新浪返回的token，类似abc123xyz456
    """
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

"""
my_key = '1163934014'
my_secret = '3830048e5d6087700e68b787c2e83c3c'
my_access_token = "2.00MIE22GQ6klQBdfe7497f230yWjCW"


my_keyword = "广埠屯"
my_keyword = my_keyword.decode('gbk').encode('utf-8')
my_client = set_weibo(my_key, my_secret, my_access_token)

r = my_client.place.pois.search.get(keyword=my_keyword, count=2, page=1)#调用新浪API
print r
"""
