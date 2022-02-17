# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import zipfile
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import WebDriverException


def get_download_link(version_chrome):
    try:
        r = requests.get("https://chromedriver.chromium.org/downloads?tmpl=/system/app/templates/print/", timeout=(5, 10))
    except Exception as e:
        print(e)

    soup = BeautifulSoup(r.text, "html.parser")

    spans = soup.find_all("span")
    for span in spans:
        enlaces = span.find_all("a", recursive=False)
        for enlace in enlaces:
            if 'ChromeDriver ' in enlace.text:
                version_enlace = enlace.text.split()[1]
                if version_enlace.split('.')[0] == version_chrome:
                    #print(f"La versión {version_enlace} está disponible para descargarse en:\n{enlace['href']}")
                    #EL ENLACE ES ASI -> https://chromedriver.storage.googleapis.com/index.html?path=90.0.4430.24/
                    splitted_version = enlace['href'].split("path=")[1].replace('/','')
                    return f"https://chromedriver.storage.googleapis.com/{splitted_version}/chromedriver_win32.zip"

def get_local_chrome_version():
    # version windows
    try:
        if 'Google' in os.listdir("C:\\Program Files\\"):
            ruta = r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get Version /value'
        else:
            ruta = r'wmic datafile where name="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" get Version /value'

        output = subprocess.check_output(
            ruta, stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
    except Exception as e:
        raise e

    # falta version ubuntu
    # subproceso con google-chrome --version

    version_chrome = output.decode('utf-8').strip().split('=')[1].split('.')[0]
    return version_chrome

def download_chromedriver(url, save_path):
    # descargar zip
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        fd.write(r.content)

    # descomprimir contenido
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall('.')

    # borramos zip
    if os.path.exists(save_path):
        os.remove(save_path)

def navegador():
    # comprobamos version de CHROMEDRIVER, si no coincide actualizamos
    actualizar, encontrado = 0, 0
    version_chrome = get_local_chrome_version()

    for file in os.listdir():
        if "chromedriver_version_" in file:
            encontrado = 1
            version_fichero = file.replace('chromedriver_version_','')
            
            # si la version es igual no descargamos una nueva
            if int(version_chrome) != int(version_fichero):
                actualizar = 1

    # si no encontramos el fichero de control
    if encontrado == 0:
        # creamos uno dummy para la proxima vez
        f = open(f"chromedriver_version_0", "w")
        f.write('')
        f.close()

        # tenemos que actualizar, por si acaso
        actualizar = 1


    if actualizar == 1:
        print("Actualizando Chromedriver...")
        download_link = get_download_link(version_chrome)
        download_chromedriver(download_link, 'chromedriver.zip')

        # eliminamos el fichero antiguo
        os.remove(f'chromedriver_version_{version_fichero}')

        # dejamos un archivo para comprobar facil la version de chrodriver y saber si actualizar
        f = open(f"chromedriver_version_{version_chrome}", "w")
        f.write('')
        f.close()
        print("Actualizado!")

    try:
        opts = Options()
        opts.add_argument("log-level=3")
        opts.add_argument("--incognito")
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        return webdriver.Chrome('chromedriver.exe', options=opts)
    except Exception as e:
        raise e