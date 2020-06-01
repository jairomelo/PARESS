# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from instapy_chromedriver import binary_path
from .sync_browser import binary_path_act
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import WebDriverException


def navegador():
    """Crea una ruta ejecutable para chromedriver"""
    try:
        return webdriver.Chrome(executable_path=binary_path)
    except SessionNotCreatedException as e:
        print("La versión de Chromedriver instalada por instapy_no corresponde a la de su navegador")
        return webdriver.Chrome(executable_path=binary_path_act)

    except WebDriverException as e:
        print("Webdriver está realizando la acción inmediatamente después de 'cerrar' el navegador.")