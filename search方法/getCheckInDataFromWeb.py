# -*- coding: utf-8 -*-


import sys
import urllib
import urllib2
import cookielib


my_cookie = 'SINAGLOBAL=8332123435102.403.1436954815196; UOR=blog.3snews.net,widget.weibo.com,www.gscloud.cn; login_sid_t=90f4ccec2f9a940192b221fd18fbbca3; _s_tentry=-; Apache=8413334940560.162.1451457387039; ULV=1451457387049:4:1:1:8413334940560.162.1451457387039:1437048393997; SUS=SID-5812120820-1451457402-GZ-1sb2m-96d94b0fe19caf44dfcc8fa15a1d9d4c; SUE=es%3Dca2f6bf165361c0841e05738e65d6da0%26ev%3Dv1%26es2%3D7a13386c06674deccc1d79ebeee0a065%26rs0%3DfFCsEHkfXqCg9zjVTK0JpnBwVJjBisr8tN0JZYskxexZtBUXfbPmJQxtAvXhbWgxx%252BAlRcGE8fGaMFmSAZK491I0ggN7DsPRR1fyr643%252FIm3XCSmQhFQenjvbBsmWtvsGEkYZ6%252FruKWaK8KXo7th39aF9RAdhFmse3TyTP%252FPzF0%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1451457402%26et%3D1451543802%26d%3Dc909%26i%3D9d4c%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D2%26st%3D0%26uid%3D5812120820%26name%3Dforweibo01%2540yeah.net%26nick%3DNotAllowed01%26fmp%3D%26lcp%3D; SUB=_2A257hwsqDeTxGeNG6lAQ8i7EyTyIHXVY9XvirDV8PUNbuNBeLVHekW9k1KHIbhtafTFs6x1-aBOYBfW2TQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5TmSGESaMP01kC3SnxgyxG5JpX5K2t; SUHB=0D-VolAfCOdRA1; ALF=1482993401; SSOLoginState=1451457402; un=forweibo01@yeah.net; wvr=6'
ua = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"
headers = {'cookie': my_cookie, 'User-Agent':ua}
url = "http://place.weibo.com/search?city=0027&city_name=%E6%AD%A6%E6%B1%89&keyword=广埠屯"
req = urllib2.Request(url, headers=headers)  #每次访问页面都带上 headers参数
response = urllib2.urlopen(req)
text = response.read()
print text
