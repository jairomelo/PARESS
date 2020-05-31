# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from instapy_chromedriver import binary_path
from selenium import webdriver


def navegador():
    """Crea una ruta ejecutable para chromedriver"""
    try:
        return webdriver.Chrome(executable_path=binary_path)
    except:
        raise


def imports():
    try:
        import reconex  # Intento de solución de errores de conexión
    except ImportError:
        # Verifica que se encuentren disponibles los archivos adicionales
        print(str(sys.exc_info()[1]),
              "No se encontró el archivo 'reconex.py'. Asegúrese de haberlo descargado y que esté en la carpeta "
              "principal del programa")
        sys.exit(-2)
