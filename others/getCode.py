# -*- coding: utf-8 -*-
from weibo import APIClient
import urllib2
import urllib
import httplib
import webbrowser

#APP_KEY和APP_SECRET，需要新建一个微博应用才能得到
APP_KEY = '1163934014'
APP_SECRET = '3830048e5d6087700e68b787c2e83c3c'
#管理中心---应用信息---高级信息，将"授权回调页"的值改成https://api.weibo.com/oauth2/default.html
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
AUTH_URL = 'https://api.weibo.com/oauth2/authorize'

def GetCode(userid,passwd):
    client = APIClient(app_key = APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    referer_url = client.get_authorize_url()
    postdata = {
        """
        "action": "login",
        "client_id": APP_KEY,
        'response_type':'code',
        "redirect_uri":CALLBACK_URL,
        "userId": userid,
        "passwd": passwd,
        """
        "action": "login",
        'display':'default',
        'withOfficalFlag':0,
        'quick_auth':'null',
        'withOfficalAccount':'',
        'scope':'',
        'ticket':'',
        'isLoginSina':'',
        'response_type':'code',
        'regCallback':'',
        'redirect_uri':CALLBACK_URL,
        'client_id':APP_KEY,
        'appkey62':'',
        'state':'',
        'verifyToken':'null',
        'from':'',
        'switchLogin':0,
        'userId':userid,
        'passwd':passwd,
        'isLoginSina':0,                
        }

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0",
        "Referer":referer_url,
        "Connection":"keep-alive",
        "Content-Type":"application/x-www-form-urlencoded"
    }
    req  = urllib2.Request(
        url = AUTH_URL,
        data = urllib.urlencode(postdata),
        headers = headers
    )
    resp = urllib2.urlopen(req)
    #return resp
    return resp.geturl()[-32:]

def get_code(username, password):
    client = APIClient(app_key = APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    referer_url = client.get_authorize_url()
    conn = httplib.HTTPSConnection('api.weibo.com')
    postdata = urllib.urlencode({"action": "login",
                                 'display':'default',
                                 'withOfficalFlag':0,
                                 'quick_auth':'null',
                                 'withOfficalAccount':'',
                                 'scope':'',
                                 'ticket':'ST-NTgxMjEyMDgyMA==-1451982449-gz-7509E3BB4C2DC05243A15BAE7C54D3A4',
                                 'isLoginSina':'',
                                 'response_type':'code',
                                 'regCallback':'https%3A%2F%2Fapi.weibo.com%2F2%2Foauth2%2Fauthorize%3Fclient_id%3D1163934014%26response_type%3Dcode%26display%3Ddefault%26redirect_uri%3Dhttps%253A%252F%252Fapi.weibo.com%252Foauth2%252Fdefault.html%26from%3D%26with_cookie%3D',
                                 'redirect_uri':CALLBACK_URL,
                                 'client_id':APP_KEY,
                                 'appkey62':'1SgvpQ',
                                 'state':'',
                                 'verifyToken':'null',
                                 'from':'',
                                 'switchLogin':0,
                                 'userId':username,
                                 'passwd':password,
                                 'isLoginSina':0, 
                                 })
    conn.request('POST','/oauth2/authorize',postdata,{'Referer':referer_url, 'Content-Type': 'application/x-www-form-urlencoded'})
    res = conn.getresponse()
    page = res.read()
    #print 'headers===========',res.getheaders()
    print 'msg===========',res.msg
    print 'status===========',res.status
    print 'reason===========',res.reason
    print 'version===========',res.version
    #print page
    #conn.close()


if __name__ == "__main__":
    #print GetCode("forweibo02@yeah.net", "789456123")
    get_code("forweibo02@yeah.net", "789456123")
