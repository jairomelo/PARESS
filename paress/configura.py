#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def imports():
	try:
		import reconex # Intento de solución de errores de conexión
		import plataforma
	except ImportError:
		# Verifica que se encuentren disponibles los archivos adicionales
		print(str(sys.exc_info()[1]),"No se encontró el archivo 'reconex.py'. Asegúrese de haberlo descargado y que esté en la carpeta principal del programa")
		sys.exit(-2)