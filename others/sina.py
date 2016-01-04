# -*- coding: utf-8 -*-
import requests
import base64
import re
import urllib
import rsa
import json
import binascii
import string
from weibo import Client
import random
import time
import logging, logging.handlers
code = "5f9f84b2aa3198032416963c84c2d182"
app_key = "4055744185"
app_secret = "838ec8be666e6116c4e483ed14e5fea4"
redirect_uri = "https://api.weibo.com/oauth2/default.html"

class SinaCrawler:
	def __init__(self, max_page):
		self.session = None
		self.MAX_PAGE = max_page
		token = {u'access_token': u'2.00pE39sBn1UT7E61e7174d95TdYVED', u'remind_in': u'157679999', u'uid': u'1720813027', u'expires_at': 1575304674}
		self.client = Client(app_key, app_secret, redirect_uri, token)
		self.f = open("data", "w")

	def __del__(self):
		self.f.close()

	def userlogin(self,username,password):
		session = requests.Session()
		url_prelogin = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.5)&_=1364875106625'
		url_login = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'
		#get servertime,nonce, pubkey,rsakv
		resp = session.get(url_prelogin)
		json_data  = re.search('\((.*)\)', resp.content).group(1)
		data       = json.loads(json_data)
		servertime = data['servertime']
		nonce      = data['nonce']
		pubkey     = data['pubkey']
		rsakv      = data['rsakv']

		# calculate su
		su  = base64.b64encode(urllib.quote(username))

		#calculate sp
		rsaPublickey= int(pubkey,16)
		key = rsa.PublicKey(rsaPublickey,65537)
		message = str(servertime) +'\t' + str(nonce) + '\n' + str(password)
		sp = binascii.b2a_hex(rsa.encrypt(message,key))
		postdata = {
			'entry': 'weibo',
			'gateway': '1',
			'from': '',
			'savestate': '7',
			'userticket': '1',
			'ssosimplelogin': '1',
			'vsnf': '1',
			'vsnval': '',
			'su': su,
			'service': 'miniblog',
			'servertime': servertime,
			'nonce': nonce,
			'pwencode': 'rsa2',
			'sp': sp,
			'encoding': 'UTF-8',
			'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
			'returntype': 'META',
			'rsakv' : rsakv,
		}
		resp = session.post(url_login,data = postdata)
		# print resp.headers
		login_url = re.findall('replace\(\'(.*)\'\)',resp.content)
		#
		respo = session.get(login_url[0])
		self.session = session
	
	def get_search_result(self, html_content):
		""" get search result from the html content 
			
		Args:
			html_content: str for storing html content of the search page
		
		Return:
			None
		"""
		#content = re.findall(r"\"pid\":\"pl_user_feedList\"(?P<tips>[\w\W]*?)", html_content)
		html_content = html_content.strip()
		content = re.findall(r"\"pid\":\"pl_wb_feedlist\"(?P<tips>[\w\W]*?)</script>", html_content)[0]		
		clean_content = string.replace(content, "\\\\", "\\")
		search_result = re.findall(r"<div class=\\\"WB_cardwrap S_bg2 clearfix\\\" >(?P<tips>[\w\W]*?)<\\/div>\\n<\\/div>", clean_content)
		return search_result

	def get_person_info(self, person_info_html):
		""" get person information from the html content

		Args:
			person_info_html : str indicating the personanl information

		Return:
			None
		"""
		txt = re.findall(r"=\\\"feed_list_content\\\">(?P<tips>[\w\W]*?)<\\/p>", person_info_html)
		content = string.replace(txt[0], '\n', '')
		content = string.replace(content, '\t', '')
		tag = True
		strs = ""
		
		for w in content:
			if w == '<':
				tag = False
				continue
			if w == '>':
				tag = True
				continue
			if tag:
				strs += w
		msg = strs.decode('unicode_escape').encode('utf8')
		msg = string.replace(msg, '\n', '')
		msg = string.replace(msg, '\t', '')
		uid = re.findall("uid=(?P<tips>\d+?)&", person_info_html)[0]
		time.sleep(random.random())
		while True:
			try:
				info_dict = self.client.get('users/show', uid = uid)
				break
			except:
				time.sleep(random.randint(1,40))
		self.f.write('%s\t%s\t%s\t%s\t%s\t' % info_dict['screen_name'].encode('utf-8'), '\t', \
			info_dict['gender'].encode('utf-8'), '\t', \
			msg, '\t',\
			info_dict['created_at'].encode('utf-8'), '\t', \
			info_dict['location'].encode('utf-8'))

	def do_search_page(self, page, query):
		""" get search result of the page in the search html page 

		Args:
			page : int indicating the number of the page

		Return:
			None
		"""
		search_url  = "http://s.weibo.com/wb/%s&page=%d" % (query, page)
		html_page = self.session.get(search_url)
		all_results = self.get_search_result(html_page.content)
		res_cnt = 1
		for res in all_results:
			print 'page %d result %d done' % (page, res_cnt)
			res_cnt += 1
			information = self.get_person_info(res)
	
	def do_search(self, query):
		""" do search 

		Args:
			query : str indicating the query 

		Return:
			None
		"""
		self.f.write('screen_name\tgender\trelated_msg\tregister_time\tlocation\n')
		for page in range(1, self.MAX_PAGE + 1):
			time.sleep(random.random())
			self.do_search_page(page, query)


if __name__ == '__main__':
	sina_crawler = SinaCrawler(50)
	user_name = raw_input("please input you username:")
	psw = raw_input("plesae input you password:")
	sina_crawler.userlogin(user_name, psw)

	query = raw_input("input the query:")
	print type(query)
	q = string.replace(str(urllib.quote(query)), "%", "%25")
	print q
	sina_crawler.do_search(q)
