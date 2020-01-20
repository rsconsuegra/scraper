# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 22:10:10 2019

@author: Randy Consuegra
"""

import re
import pickle
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def content_scrapper(url,rule,element,element_attribute):
	page = requests.get(url,verify = False)
	soup = BeautifulSoup(page.text, 'html.parser')
	
	regex = re.compile(rule)
	content_element = soup.find_all(element, attrs={element_attribute : regex})
	return content_element



urls = [
		"https://www.ecccomics.com/comics/universo-dc-48.aspx",
		"https://www.ecccomics.com/comics/dc-deluxe-4095.aspx",
		"https://www.ecccomics.com/comics/dc-black-label-3906.aspx",
		"https://www.ecccomics.com/comics/dc-xp-4096.aspx",
		"https://www.ecccomics.com/comics/watchmen-4120.aspx",
		"https://www.ecccomics.com/comics/vertigo-50.aspx",
		"https://www.ecccomics.com/comics/coleccionables-3140.aspx",
		"https://www.ecccomics.com/comics/otros-titulos-de-dc-1989.aspx",
		"https://www.ecccomics.com/comics/autor-1410.aspx",
		"https://www.ecccomics.com/comics/manga-1351.aspx",
		"https://www.ecccomics.com/comics/literatura-1367.aspx",
		"https://www.ecccomics.com/comics/crossroads-1425.aspx"
		]

pages=[]

for url in urls:
	content_ul = content_scrapper(
			url=url,
			rule='^subcat',
			element='ul',
			element_attribute = 'class')
	print("Getting info")
	content = []
	
	for ul in content_ul:
		for a_tag in ul.findAll('a'):
			content.append(a_tag.get('href'))
	
	for index in content:
		seps = content_scrapper(
				url=index,
				rule='.*LinkPagina$',
				element='a',
				element_attribute = 'id')
		
		pages.append(index)
		
		if len(seps) > 0:
			for sep in seps:
				pages.append(sep.get('href'))
				
	print(len(pages))

# Dict key is the comic name, the value is the URL
titles = {}
print("Getting titles")
for page in pages:
	for title in content_scrapper(
			url=page,
			rule='titprod',
			element='span',
			element_attribute = 'class'):
		#titles.append(title.find('a').get('href'))
		titles[title.find("a").get_text()] = title.find('a').get('href')

with open('comics.pickle', 'wb') as handle:
	print("Writing pickle")
	pickle.dump(titles, handle, protocol=pickle.HIGHEST_PROTOCOL)
	print("Pickle writed successfully")
