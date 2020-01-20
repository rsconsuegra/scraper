# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 21:57:18 2019

@author: Randy Consuegra
"""

from lxml import html
import requests
import locale

CONV = 4100
SHIFT = 12000

def get_autores(xpath):	
	element_autor = tree.xpath(xpath)
	autor = ''
	for element in element_autor[0]:
		if ',' in element.text:
			autors = element.text.split(',')
			autor = ',' + autors[1].strip() + ' ' + autors[0] + autor
		else:
			autor = ',' + element.text + autor
	
	return autor[1:]

def currency(value):
	locale.setlocale(locale.LC_ALL, 'es')
	euro_to_peso = locale.atof(value.strip('€'))
	return '${0}'.format(locale.format_string('%d', euro_to_peso*CONV+SHIFT, True))
	
if __name__ == "__main__":
	
	page = requests.get('http://sddistribuciones.com/OJO-DE-HALCON-DE-MATT-FRACTION-Y-DAVID-AJA-Isbn-978-84-9167-836-6-Codigo-MEX,SMAIN020')
	tree = html.fromstring(page.content)
	
	comic ={}
	
	comic['Estado'] = tree.xpath('//*[@id="ContentPlaceHolder1_lblEstado"]')[0].text
	comic['Titulo'] = tree.xpath('//*[@id="ContentPlaceHolder1_lblTitulo"]')[0].text
	comic['Autor(es)'] = get_autores('//*[@id="ContentPlaceHolder1_lblAutor_comic"]')
	comic['Precio(EUR)'] = tree.xpath('//*[@id="ContentPlaceHolder1_lblPVP"]')[0].text
	comic['Precio(COP)'] = currency(comic['Precio(EUR)'])
	comic['Encuadernacion'] = tree.xpath('//*[@id="ContentPlaceHolder1_lblEncuadernacion_comic"]')[0].text
	comic['Pags'] = tree.xpath('//*[@id="ContentPlaceHolder1_lblPaginas_comic"]')[0].text
	comic['Editorial'] = tree.xpath('//*[@id="ContentPlaceHolder1_lblEditorial_comic"]')[0][0].text
	comic['Coleccion'] = tree.xpath('//*[@id="ContentPlaceHolder1_lblColeccion_comic"]')[0].text
	
	print(comic)