# -*- coding: UTF-8 -*-
"""
 获取时光影评电影评分排行榜
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 获得指定开始排行的电影url
def get_url(root_url,start):
	#return root_url+"?start="+str(start)+"&filter="
	return root_url+"?params={%22offset%22:"+str(start)+",%22type%22:%22day%22}"


def get_review(page_url):
	movies_list=[]
	#请求url，返回response对象
	headers = {'content-type': 'text/html','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	response=requests.get(page_url,headers=headers)
	#指定lxml解析器解析html文档
	soup=BeautifulSoup(response.text,"lxml")
	#获取包含所有电影信息的节点
	#soup=soup.find('body')
	#循环获取单个节点
	for tag_li in soup.find_all('div','feed-item'):
		dict={}
		#dict['rank']=tag_li.find('em').string
		dict['name']=tag_li.find_all('a','question_link')[0].string
		if(tag_li.find_all('a','author-link')):
			dict['author']=tag_li.find_all('a','author-link')[0].string
		else:
			dict['author']="未知"
		dict['score']=tag_li.find('span','count').string
		#有的电影短评为空，为防止抓取到一半出错，需判断是否为空
		#if(tag_li.find('span','inq')):
		#dict['desc']=tag_li.find('span','inq').string
		movies_list.append(dict)
	return movies_list

if __name__ == "__main__":
	#root_url="https://movie.douban.com/top250"
	root_url="https://www.zhihu.com/node/ExploreAnswerListV2"
	start=0
	while(start<20):
		movies_list=get_review(get_url(root_url,start))
		for movie_dict in movies_list:
			#print(movies_list)
			#这里就可以循环插入数据库了
			#print('电影排名：'+movie_dict['rank'])
			print('问题：'+movie_dict.get('name'))
			print('回答者：'+movie_dict.get('author'))
			print('赞同数：'+movie_dict.get('score'))
			#print('电影评词：'+movie_dict.get('desc','无评词'))
			print('------------------------------------------------------')
		start += 5

