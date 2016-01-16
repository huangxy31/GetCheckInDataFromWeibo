#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from libs.weibo import APIClient
import webbrowser#python内置的包

access_token_file = open('../libs/accessToken.txt', 'a')


'''
APP_KEY = '1163934014'
APP_SECRET = '3830048e5d6087700e68b787c2e83c3c'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
'''
def get_access_token(APP_KEY, APP_SECRET, CALLBACK_URL):
    #利用官方微博SDK
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    #得到授权页面的url，利用webbrowser打开这个url
    url = client.get_authorize_url()
    print url
    webbrowser.open_new(url)
    #获取code=后面的内容
    print '输入url中code后面的内容后按回车键：'
    code = raw_input()
    #code = your.web.framework.request.get('code')
    #client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token # 新浪返回的token，类似abc123xyz456
    access_token_file.write(str(access_token)+'\n')
    print access_token
    expires_in = r.expires_in
    print expires_in

app_info_list = []
f = open('../libs/appKey.txt', 'r')
for line in f:
    app_info_list.append(line[:-1].split(','))

CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
for app_info in app_info_list:
    APP_KEY = app_info[0]
    APP_SECRET = app_info[1]
    get_access_token(APP_KEY, APP_SECRET, CALLBACK_URL)

f.close()
access_token_file.flush()
access_token_file.close()
