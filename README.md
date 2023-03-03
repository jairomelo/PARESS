# :warning::lock_with_ink_pen: Este proyecto está archivado

La nueva versión del programa es [paress2](https://github.com/jairomelo/paress2). También se puede instalar desde PyPi con:

`pip install paress2`

## Una pequeña nota sobre el cierre de este repositorio

Este fue mi primer proyecto real de programación con Python. Fue una experiencia interesantísima poder crear un programa que pudiera ser utilizado por otras personas y que de hecho ayudó a varios a obtener la información necesaria para realizar sus investigaciones, tesis de maestría y doctorado, o simplemente para tener un respaldo de lo que en un momento dado podría eliminarse por un capricho institucional.

La experiencia de creación fue interesante, pero también estuvo llena de errores. El código en general es muy difícil de mantener y con cada actualización del Portal de Archivos Españoles la actualización era un dolor de cabeza. Básicamente el proyecto estuvo sin funcionar por lo menos un año debido a una actualización simple en la interfaz del archivo.

Por esa razón he decidido que era mejor rehacer el programa antes que intentar reformarlo. El nuevo programa se encuentra en [paress2](https://github.com/jairomelo/paress2) y es mucho más ligero, funcional y fácil de mantener. Con esto será posible escalar el proyecto y hacer frente a las actualizaciones del PARES de manera más rápida.

# PARESS - Web Scraping el Portal de Archivos Españoles

Este es un módulo que puede ser utilizado para realizar tareas de *Web Scraping* en el Portal de Archivos Españoles.

# Instalación

Desde PyPI

`pip install paress`

Desde GitHub

`pip install git+https://github.com/jairomelo/PARESS.git`

# Uso

Un video tutorial para la descarga de imágenes fue publicado por Carlos Díaz: https://www.youtube.com/watch?v=HTEQtytLV-U

paress.**metadatalist**(url,elem,host="http://pares.mcu.es")

Regresa un lista de un elemento: título, fecha, signatura, archivo.
El parámetro *elem* se debe indicar como sigue:
	* Título de los elementos: "titulo"
	* Nombre de los archivos: "archivo"
	* Fechas: "fecha"
	* Signaturas: "signatura"

*Ej.: Cartas y expedientes de personas eclesiásticas, sig. FILIPINAS,301*

```python
import paress

paress.metadatalist("http://pares.mcu.es/ParesBusquedas20/catalogo/contiene/425393","fecha")

```

paress.**imagenes**(url, ident="descarga", host="http://pares.mcu.es")

Descarga las imágenes de un expediente. La ruta debe ser "http://pares.mcu.es/ParesBusquedas20/catalogo/show/xxx".
Puede personalizarse el nombre del archivo de la descarga con el parámetro *ident*. *En caso de no incluir este parámetro el programa descarga las imágenes en el directorio '/descarga/' y reemplaza cualquier archivo con el nombre 'descarga.csv'.* Nombres muy largos pueden generar errores.

*Ej: Registro: Virreyes de Santa Fe, sig. Archivo General de Indias, SANTA_FE,541,L.3*

```python
import paress

paress.imagenes("http://pares.mcu.es/ParesBusquedas20/catalogo/show/384442","nombre_directorio")

```

paress.**metadata**(url,ident="descarga",host="http://pares.mcu.es")

Descarga el conjunto de metadatos en un archivo csv.
Puede personalizarse el nombre del archivo de la descarga con el parámetro *ident*. *En caso de no incluir este parámetro el programa descarga las imágenes en el directorio '/descarga/' pero no reemplaza ninguna imagen.* Nombres muy largos pueden generar errores.

*Ej.: Cartas y expedientes de personas eclesiásticas, sig. FILIPINAS,301*

```python
import paress

paress.metadata("http://pares.mcu.es/ParesBusquedas20/catalogo/contiene/425393","nombre_directorio")

```

El parámetro URL en `paress.metadata()` y `pares.metadatalist()` acepta cualquier ruta que contenga un listado, ya sea una búsqueda simple, avanzada, listado de autoridad o unidad documental.
