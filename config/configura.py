#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def imports():
	try:
		from selenium import webdriver
		from selenium.webdriver.common.keys import Keys
		from bs4 import BeautifulSoup
	except ImportError:
		# Verifica la instalación de los módulos requeridos
		print((os.linesep * 2).join(["No fue posible importar el módulo:", 
			str(sys.exc_info()[1]), "Debe instalarlo para poder correr el programa [Ver ayuda en: https://programminghistorian.org/es/lecciones/instalar-modulos-python-pip]", "Saliendo del programa..."]))
		sys.exit(-2)

	try:
		import reconex # Intento de solución de errores de conexión
		import plataforma
	except ImportError:
		# Verifica que se encuentren disponibles los archivos adicionales
		print(str(sys.exc_info()[1]),"No se encontró el archivo 'reconex.py'. Asegúrese de haberlo descargado y que esté en la carpeta principal del programa")
		sys.exit(-2)