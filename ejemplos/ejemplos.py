#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Librerías standar de Python 3
import PARES_scrap

#########################################################################

#ident = input('Ingresar número del expediente: ')
#ident = "4633387" # imágenes
#ident = "121075" # colección
ident = "perdón" # búsqueda simple
#########################################################################
# Imágenes
host = 'http://pares.mcu.es'
#ruta_entrada = '/ParesBusquedas20/catalogo/show/{}'.format(ident)
#url_entrada = '{}{}'.format(host, ruta_entrada)

#########################################################################
# Metadata colecciones
#ruta_entrada = '/ParesBusquedas20/catalogo/contiene/{}'.format(ident)
#url_entrada = '{}{}'.format(host, ruta_entrada)

#########################################################################
# Metadata texto
host = 'http://pares.mcu.es'
ruta_entrada = '/ParesBusquedas20/catalogo/find?texto={}'.format(ident)
url_entrada = '{}{}'.format(host, ruta_entrada)

#########################################################################

#PARES_scrap.imagenes(url_entrada, ident)

#PARES_scrap.metadata(url_entrada,ident)
url = "http://pares.mcu.es/ParesBusquedas20/catalogo/find?texto=indulto&archivo=10&dia1=01&mes1=01&anio1=1650&fechaInicio=1650-01-01&dia2=31&mes2=12&anio2=1850&fechaFin=1850-12-31"

PARES_scrap.metadata(url,"carpeta_de_Jairo")