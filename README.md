# PARESS - Web Scraping el Portal de Archivos Españoles

Este es un módulo que puede ser utilizado para realizar tareas de *Web Scraping* en el Portal de Archivos Españoles.

# Instalación

Desde PyPI

`pip install paress`

Desde GitHub

`pip install git+https://github.com/jairomelo/PARESS.git`

# Uso

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
Puede personalizarse el nombre del archivo de la descarga con el parámetro *ident*. *En caso de no incluir este parámetro el programa descarga las imágenes en el directorio '/descarga/' y reemplaza cualquier archivo con el nombre 'descarga.csv'.*

*Ej: Registro: Virreyes de Santa Fe, sig. Archivo General de Indias, SANTA_FE,541,L.3*

```python
import paress

paress.imagenes("http://pares.mcu.es/ParesBusquedas20/catalogo/show/384442","384442")

```

paress.**metadata**(url,ident="descarga",host="http://pares.mcu.es")

Descarga el conjunto de metadatos en un archivo csv.
Puede personalizarse el nombre del archivo de la descarga con el parámetro *ident*. *En caso de no incluir este parámetro el programa descarga las imágenes en el directorio '/descarga/' pero no reemplaza ninguna imagen.*

*Ej.: Cartas y expedientes de personas eclesiásticas, sig. FILIPINAS,301*

```python
import paress

paress.metadata("http://pares.mcu.es/ParesBusquedas20/catalogo/contiene/425393","425393")

```

El parámetro URL en `paress.metadata()` y `pares.metadatalist()` acepta cualquier ruta que contenga un listado, ya sea una búsqueda simple, avanzada, listado de autoridad o unidad documental.
