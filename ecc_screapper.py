# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 15:13:39 2020

@author: Randy Consuegra
"""

import re
import pickle
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(
		urllib3
		.exceptions
		.InsecureRequestWarning)

import locale
from datetime import datetime,date,timedelta

CONV = 4100
SHIFT = 12000

def content_scrapper(soup,rule,element,element_attribute):
	
	
	regex = re.compile(rule)
	content_element = soup.find_all(
			element,
			attrs={element_attribute : regex})
	return content_element

def search_title(df,title_name):
	df[df.index.str.startswith(title_name)]

def currency(value):
	locale.setlocale(locale.LC_ALL, 'es')
	euro_to_peso = locale.atof(value.strip('€'))
	return '${0}'.format(
			locale.format_string(
					'%d', 
					euro_to_peso*CONV+SHIFT, True)
			)
	

if __name__ == "__main__":
	with open('comics.pickle', 'rb') as handle:
		ECC_comics = pickle.load(handle)
	
	comics = pd.DataFrame()
	ECC = pd.Series(ECC_comics)
	
	comic = {}
	comic['Editorial'] = "ECC"
	
	for product in ECC:
		
		page = requests.get(product,verify = False)
		soup = BeautifulSoup(page.text, 'html.parser')
		
		info = content_scrapper(
				soup=soup,
				rule='infoprod',
				element='div',
				element_attribute = 'class')
		
		attributes = (info[0].text
				.replace("\n","")
				.replace("\r","")
				.split(" || ")
				)
		if (not "GUIÓN" in info[0].text):
			attributes.insert(2,f'GUIÓN: NA')

		if (not "DIBUJO" in info[0].text):
			attributes.insert(3,f'DIBUJO: {attributes[2][7:]}')
			
		attributes[-1] = attributes[-1].rstrip()
		
		if(len(attributes)>4):
			edi = re.split(r'[:,]|\.\s',attributes[4])[1:]
		else:
			edi = ["NA","NA"]
		
		if len(edi) > 3:
			publication_date = datetime.strptime(
					edi[-1][-10:],'%d/%m/%Y').date()
		else:
			publication_date = date.today() - timedelta(days=1)
			
		
		
		estado = content_scrapper(
				soup = soup,
				rule = "ctl00_ContentPlaceHolder1_LitMensaje",
				element="span",
				element_attribute="id")[0].text
		
		if len(estado)<2:	
			comic['Estado'] = "Disponible"
		else:
			if(publication_date < date.today()):
				comic['Estado'] = "AGOTADO"
			else:
				comic['Estado'] = "Proximamente"
	
		comic['Titulo'] = content_scrapper(
				soup = soup,
				rule = "titprod",
				element="span",
				element_attribute="class")[0].text
				
		comic['Autor(es)'] = (attributes[2].split(": ")[1] 
				+ ", " + attributes[3].split(": ")[1])
		
		comic['Precio(EUR)'] = (content_scrapper(
					soup =soup,
					rule='precio',
					element='div',
					element_attribute = 'class')[0]
				.text.replace("\n","")
				.replace("\r","")
				.strip()
				)
		
		comic['Precio(COP)'] = currency(comic['Precio(EUR)'])
		
		comic['Encuadernacion'] = edi[0].strip()
		
		comic['Pags'] = edi[1].strip()
				
		comics = comics.append(comic, ignore_index=True)

		print(f"{comic['Titulo']} Loaded")
	
	with open('Comics_DataFrame.json', 'w', encoding='utf-8') as file:
			comics.to_json(file, orient='index', force_ascii=False)