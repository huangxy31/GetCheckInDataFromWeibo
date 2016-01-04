#coding=utf8
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib

#获取一个保存cookie的对象
cj = cookielib.LWPCookieJar()
#将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
cookie_support = urllib2.HTTPCookieProcessor(cj)
#创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
#将包含了cookie、http处理器、http的handler的资源和urllib2对象板顶在一起
urllib2.install_opener(opener)

postdata = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'userticket': '1',
    'ssosimplelogin': '1',
    'vsnf': '1',
    'vsnval': '',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'wsse',
    'sp': '',
    'encoding': 'UTF-8',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack', 'returntype': 'META'
}

def get_servertime():

    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)&_=1329806375939'
    data = urllib2.urlopen(url).read()
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        return servertime, nonce
    except:
        print 'Get severtime error!'
        return None

def get_pwd(pwd, servertime, nonce):
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3_ = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd3_).hexdigest()
    return pwd3

def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username

def main():
    global postdata
    username = 'forweibo01@yeah.net'#微博账号
    pwd = '789456123'#微博密码
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
    try:
        servertime, nonce = get_servertime()
    except:
        #return global postdata
        return postdata
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd, servertime, nonce)
    postdata = urllib.urlencode(postdata)
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    #其实到了这里，已经能够使用urllib2请求新浪任何的内容了，这里已经登陆成功了
    req  = urllib2.Request(
        url = url,
        data = postdata,
        headers = headers
    )
    result = urllib2.urlopen(req)
    text = result.read()
    #print text
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        login_url = p.search(text).group(1)
        print login_url
        #print login_url
        urllib2.urlopen(login_url)
        print "login success"
    except:
        print 'Login error!'
    #测试读取数据，下面的URL，可以换成任意的地址，都能把内容读取下来
    req = urllib2.Request(url='http://e.weibo.com/aj/mblog/mbloglist?page=1&count=15&max_id=3463810566724276&pre_page=1&end_id=3458270641877724&pagebar=1&_k=134138430655960&uid=2383944094&_t=0&__rnd=1341384513840',)
    result = urllib2.urlopen(req)
    text = result.read()
    print len(result.read())
    #unicode(eval(b),"utf-8")
    print eval("u'''"+text+"'''") 
main()
