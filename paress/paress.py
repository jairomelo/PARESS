#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, time, os, urllib, codecs, sys, csv
import configura

configura.imports()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import reconex # Intento de solución de errores de conexión
import plataforma

plataforma.check_install()

local = os.getcwd()

def version():
	print("0.0.146")

def imagenes(url, ident="descarga", host="http://pares.mcu.es"):
	"""
	Ejecuta un script para descargar las imágenes en un directorio.
	url = dirección completa del enlace
	ident = número de identificación del expediente
	host = 'http://pares.mcu.es'
	"""
	browser = plataforma.navegador()
	browser.get(url)

	#########################################################################

	soup = BeautifulSoup(browser.page_source, 'html.parser')

	#########################################################################
	## Obtener la cantidad de imágenes y el rango

	num_pags = soup.select("span", {"class": "numPag"})
	lines = [span.get_text() for span in num_pags]
	num_imgs = lines[4]
	rango = int(num_imgs)/8

	#########################################################################
	## Obtener los enlaces de las imágenes

	imgs = soup.select("div.thumbnail img")

	rutas = []

	#primera página
	for img in imgs:
		obtener = "{}{}".format(host, img["src"])
		rutas.append(obtener)

	#resto de páginas
	for i in range(int(rango)):
		i = browser.find_element_by_xpath('//*[@id="botonMasPeq"]')
		i.click()
		time.sleep(1)
		soup = BeautifulSoup(browser.page_source, 'html.parser')
		imgs = soup.select("div.thumbnail img")
		for img in imgs:
			obtener = "{}{}".format(host, img["src"])
			rutas.append(obtener)

	browser.quit()

	#########################################################################
	## Manipulación de la lista para crear los enlaces de descarga

	cadenas = str(rutas)
	encadenado = ''.join(cadenas).replace('[\'','').replace('\']',',').replace('&txt_transformacion=0','').replace('\'','').replace('&txt_contraste=0', '&txt_zoom=10&txt_contraste=0&txt_polarizado=&txt_brillo=10.0&txt_contrast=1.0')
	mi_cadena = encadenado.split(",")
	
	#########################################################################
	## Crea el directorio y empieza la descarga de imágenes

	from datetime import timedelta # solo para desarrollo

	if not os.path.exists('{}/descargas/{}'.format(local,ident)):
		os.makedirs('{}/descargas/{}'.format(local,ident))

	inicio_loop = time.time() # Desarrollo : tiempo que toma en ejecutarse el programa
	for i in range(len(rutas)):
		start = time.time()
		if not os.path.exists("{}/descargas/{}/{}.jpg".format(local,ident, i+1)):
			s = requests.Session()
			read = reconex.requests_retry_session(session=s).get(url) # Intento de solución de errores de conexión
			url_descarga = mi_cadena[i]
			read = reconex.requests_retry_session(session=s).get(url_descarga) # Intento de solución de errores de conexión
			with open("{}/descargas/{}/{}.jpg".format(local,ident, i+1), 'wb') as handler:
				handler.write(read.content)
				print("Descargando la imagen {}.jpg de {}".format(i+1, num_imgs))
				lapso = (time.time() - start) # Desarrollo : tiempo que toma en ejecutarse el programa
				print("Descargada en {} segundos".format(lapso)) # Desarrollo : tiempo que toma en ejecutarse el programa
				time.sleep(1)

	lapso_loop = (time.time() - inicio_loop) # Desarrollo : tiempo que toma en ejecutarse el programa
	horminsec = str(timedelta(seconds=lapso_loop))
	print("Descargadas {} imágenes en {}".format(num_imgs,horminsec))

	#########################################################################
	# Obtener página de descripción

	url_descripcion = '{}/ParesBusquedas20/catalogo/description/{}'.format(host, ident)
	salsa = urllib.request.urlopen(url_descripcion).read()
	sopa = BeautifulSoup(salsa, 'html.parser')
	f = codecs.open('{}/descargas/{}/{}.html'.format(local,ident, ident), "w+", "utf-8")
	for div in sopa.find_all('div', {'id': 'contenido_interior_ficha'}):
		f.write(div.prettify())

	print("Descarga completa en la carpeta descargas/{}".format(ident))

"""

Esta es una función para descargar los metadatos de una colección de documentos.

"""

def metapages(soup):

	num_pages = soup.select("span", {"class": "azul"})
	lines = [span.get_text() for span in num_pages]
	if lines[4] == "Aviso Legal":
		num_pags = 1
	else:
		num_pag = lines[9]
		num_pag1 = ''.join(num_pag).replace('.','')
		num_pag2 = int(num_pag1)/25
		num_pags = round(num_pag2)+1
		rango = num_pags-2
		pag_rest = num_pags+2
	
	return num_pags

def metadata(url,ident="descarga",host="http://pares.mcu.es"):
	"""
	Ejecuta el script para descargar metadata de una colección.
	url = dirección completa del enlace
	ident = número de identificación de la colección
	host = 'http://pares.mcu.es'
	"""

	browser = plataforma.navegador()
	browser.get(url)
	
	soup = BeautifulSoup(browser.page_source, 'html.parser')

	num_pags = metapages(soup)
	rango = num_pags-2
	pag_rest = num_pags+2

	## Listados que serán columnas en el csv

	listado = []
	tipolist = []
	signalist = []
	titulist = []

	## Loops para recuperar los elementos

	if num_pags == 1:
		#soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select('p.fecha')
			for columns in total:
				fecha = columns.get_text()
				listado.append(fecha)
			archi = box.select('p.tipo_archivo')
			for columns in archi:
				tip = columns.get_text()
				tipolist.append(tip)
			signa = box.select('p.signatura')
			for columns in signa:
				signat = columns.get_text()
				signalist.append(signat)
			titul = box.select('p.titulo a')
			for columns in titul:
				titu = columns.get_text()
				titulist.append(titu)

	#########################
	###si el número de págs está entre 2 y 5
	#########################

	elif num_pags in range(1,6):
	# page 1
		#soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select('p.fecha')
			for columns in total:
				fecha = columns.get_text()
				listado.append(fecha)
			archi = box.select('p.tipo_archivo')
			for columns in archi:
				tip = columns.get_text()
				tipolist.append(tip)
			signa = box.select('p.signatura')
			for columns in signa:
				signat = columns.get_text()
				signalist.append(signat)
			titul = box.select('p.titulo a')
			for columns in titul:
				titu = columns.get_text()
				titulist.append(titu)
		#page 2
		ruti = browser.find_element_by_xpath('//*[@id="resultados"]/div[2]/a[{}]'.format(num_pags))
		ruti.click()
		time.sleep(1)
		#soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select('p.fecha')
			for columns in total:
				fecha = columns.get_text()
				listado.append(fecha)
			archi = box.select('p.tipo_archivo')
			for columns in archi:
				tip = columns.get_text()
				tipolist.append(tip)
			signa = box.select('p.signatura')
			for columns in signa:
				signat = columns.get_text()
				signalist.append(signat)
			titul = box.select('p.titulo a')
			for columns in titul:
				titu = columns.get_text()
				titulist.append(titu)
		# resto de págs //*[@id="resultados"]/div[2]/a[5]
		for i in range(rango):
			i = browser.find_element_by_xpath('//*[@id="resultados"]/div[2]/a[{}]'.format(pag_rest))
			i.click()
			time.sleep(5)
			#soup = BeautifulSoup(browser.page_source, 'html.parser')
			for em in soup("em"):
				soup.em.decompose()
			caja = soup.select('table.displayTable tbody')
			for box in caja:
				total = box.select('p.fecha')
				for columns in total:
					fecha = columns.get_text()
					listado.append(fecha)
				archi = box.select('p.tipo_archivo')
				for columns in archi:
					tip = columns.get_text()
					tipolist.append(tip)
				signa = box.select('p.signatura')
				for columns in signa:
					signat = columns.get_text()
					signalist.append(signat)
				titul = box.select('p.titulo a')
				for columns in titul:
					titu = columns.get_text()
					titulist.append(titu)

	#########################
	### si el número de págs es mayor a 5
	#########################

	elif num_pags > 5:
		# page 1
		soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select('p.fecha')
			for columns in total:
				fecha = columns.get_text()
				listado.append(fecha)
			archi = box.select('p.tipo_archivo')
			for columns in archi:
				tip = columns.get_text()
				tipolist.append(tip)
			signa = box.select('p.signatura')
			for columns in signa:
				signat = columns.get_text()
				signalist.append(signat)
			titul = box.select('p.titulo a')
			for columns in titul:
				titu = columns.get_text()
				titulist.append(titu)
		# page 2
		time.sleep(1)
		ruti = browser.find_element_by_xpath('//*[@id="resultados"]/div[2]/a[5]')
		ruti.click()
		time.sleep(3)
		soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select('p.fecha')
			for columns in total:
				fecha = columns.get_text()
				listado.append(fecha)
			archi = box.select('p.tipo_archivo')
			for columns in archi:
				tip = columns.get_text()
				tipolist.append(tip)
			signa = box.select('p.signatura')
			for columns in signa:
				signat = columns.get_text()
				signalist.append(signat)
			titul = box.select('p.titulo a')
			for columns in titul:
				titu = columns.get_text()
				titulist.append(titu)
		# resto de págs
		time.sleep(3)
		for i in range(rango):
			i = browser.find_element_by_xpath('//*[@id="resultados"]/div[2]/a[7]')
			i.click()
			time.sleep(5)
			soup = BeautifulSoup(browser.page_source, 'html.parser')
			for em in soup("em"):
				soup.em.decompose()
			caja = soup.select('table.displayTable tbody')
			for box in caja:
				total = box.select('p.fecha')
				for columns in total:
					fecha = columns.get_text()
					listado.append(fecha)
				archi = box.select('p.tipo_archivo')
				for columns in archi:
					tip = columns.get_text()
					tipolist.append(tip)
				signa = box.select('p.signatura')
				for columns in signa:
					signat = columns.get_text()
					signalist.append(signat)
				titul = box.select('p.titulo a')
				for columns in titul:
					titu = columns.get_text()
					titulist.append(titu)
	else:
		print("ERROR")
		time.sleep(3)

	# Finalizar el navegador
	browser.quit()

	###########################################################################
	## Crea el directorio

	if not os.path.exists('{}/metadata/{}'.format(local,ident)):
		os.makedirs('{}/metadata/{}'.format(local,ident))

	#########################################################################
	## Convertir el resultado en *.csv

	with open('{}/metadata/{}/{}.csv'.format(local,ident, ident), "w", newline="") as csv_file:
		fieldnames = ['Título','Fecha','Signatura','Archivo']
		writer_h = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer_h.writeheader()
		writer = csv.writer(csv_file)
		writer.writerows(zip(titulist,listado,signalist,tipolist))

	##########################################################################

	time.sleep(3)
	sys.exit(0)

"""

Esta función regresa la lista de un elemento

"""


def metadatalist(url,elem,host="http://pares.mcu.es"):
	"""
	Regresa una lista de elementos en una colección
	url = dirección completa del enlace
	elemento = titulo, archivo, fecha, signatura
	host = 'http://pares.mcu.es'
	"""
	if elem == "titulo":
		divid = 'p.titulo a'
	elif elem == "archivo":
		divid = 'p.tipo_archivo'
	elif elem == "fecha":
		divid = 'p.fecha'
	elif elem == "signatura":
		divid = 'p.signatura'
	else:
		print("ERROR: El elemento no fue indicado correctamente.")
		input("ENTER para salir")
		sys.exit()

	browser = plataforma.navegador()
	browser.get(url)
	
	soup = BeautifulSoup(browser.page_source, 'html.parser')

	num_pags = metapages(soup)
	rango = num_pags-2
	pag_rest = num_pags+2

	## Listados que serán columnas en el csv

	listado = []

	## Loops para recuperar los elementos

	if num_pags == 1:
		#soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select(divid)
			for columns in total:
				element = columns.get_text()
				listado.append(element)

	#########################
	###si el número de págs está entre 2 y 5
	#########################

	elif num_pags in range(1,6):
	# page 1
		#soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select(divid)
			for columns in total:
				element = columns.get_text()
				listado.append(element)
		#page 2
		ruti = browser.find_element_by_xpath('//*[@id="resultados"]/div[2]/a[{}]'.format(num_pags))
		ruti.click()
		time.sleep(1)
		#soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select(divid)
			for columns in total:
				element = columns.get_text()
				listado.append(element)
		# resto de págs //*[@id="resultados"]/div[2]/a[5]
		for i in range(rango):
			i = browser.find_element_by_xpath('//*[@id="resultados"]/div[2]/a[{}]'.format(pag_rest))
			i.click()
			time.sleep(5)
			#soup = BeautifulSoup(browser.page_source, 'html.parser')
			for em in soup("em"):
				soup.em.decompose()
			caja = soup.select('table.displayTable tbody')
			for box in caja:
				total = box.select(divid)
				for columns in total:
					element = columns.get_text()
					listado.append(element)

	#########################
	### si el número de págs es mayor a 5
	#########################

	elif num_pags > 5:
		# page 1
		soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select(divid)
			for columns in total:
				element = columns.get_text()
				listado.append(element)
		# page 2
		time.sleep(1)
		ruti = browser.find_element_by_xpath('//*[@id="resultados"]/div[2]/a[5]')
		ruti.click()
		time.sleep(3)
		soup = BeautifulSoup(browser.page_source, 'html.parser')
		for em in soup("em"):
			soup.em.decompose()
		caja = soup.select('table.displayTable tbody')
		for box in caja:
			total = box.select(divid)
			for columns in total:
				element = columns.get_text()
				listado.append(element)
		# resto de págs
		time.sleep(3)
		for i in range(rango):
			i = browser.find_element_by_xpath('//*[@id="resultados"]/div[2]/a[7]')
			i.click()
			time.sleep(5)
			soup = BeautifulSoup(browser.page_source, 'html.parser')
			for em in soup("em"):
				soup.em.decompose()
			caja = soup.select('table.displayTable tbody')
			for box in caja:
				total = box.select(divid)
				for columns in total:
					element = columns.get_text()
					listado.append(element)
	else:
		print("ERROR")
		time.sleep(3)

	# Finalizar el navegador
	browser.quit()

	return listado