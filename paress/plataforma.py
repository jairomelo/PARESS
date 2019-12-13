import os
import platform

from compatibilidad import install_chromedriver
from selenium import webdriver

plataforma = platform.system()


def check_install():
    """Comprueba que chromedriver esté disponible en la carpeta 'bin' """
    if plataforma == "Windows":
        if not os.path.exists('bin/chromedriver.exe'):
            install_chromedriver()
    else:
        if not os.path.exists('bin/chromedriver'):
            install_chromedriver()


def navegador():
    """Crea una ruta ejecutable para chromedriver"""
    if plataforma == "Windows":
        return webdriver.Chrome(executable_path=r'bin/chromedriver.exe')
    else:
        return webdriver.Chrome(executable_path=r'bin/chromedriver')
