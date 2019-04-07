import os, sys
import platform
import shutil
from zipfile import ZipFile
import urllib.request
from selenium import webdriver

"""
Algunas variables que pueden ser útiles en caso de requerir la versión del software y su arquitectura
"""

#SO = os.name
plataforma = platform.system()
#vplataforma = platform.release()
#arch = platform.architecture()
#plataformada = "Este programa está corriendo en {} / {} {} de {}".format(SO, plataforma,vplataforma,arch)

local_path = 'bin/chromedriver.zip'

def get_chromedriver_url(version='73.0.3683.68'): # La versión 73 es compatible con mi Google Chrome browser
    """
    Generates the download URL for current platform , architecture and the given version. Default version is 74.0.3729.6.
    Supports Linux, MacOS and Windows.
    :param version: chromedriver version string, default '74.0.3729.6'
    :return: Download URL for chromedriver
    """
    base_url = 'https://chromedriver.storage.googleapis.com/'
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        platform = 'mac'
        architecture = '64'
    elif sys.platform.startswith('win'):
        platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return base_url + version + '/chromedriver_' + platform + architecture + '.zip'

def makdirect(SO):
	if SO == "win":
		if not os.path.exists('bin/chromedriver.exe'):
			os.makedirs('bin')
	else:
		if not os.path.exists('bin/chromedriver'):
			os.makedirs('bin')

def install_chromedriver():
	"""De acuerdo con la plataforma, descarga chromedriver en la carpeta 'bin' """

	if plataforma == "Windows":
		print("Espere mientras se descarga chromedriver")
		url = get_chromedriver_url()
		makdirect("win")
		urllib.request.urlretrieve(url, local_path)
	elif plataforma == "Linux":
		print("Espere mientras se descarga chromedriver")
		url = get_chromedriver_url()
		makdirect("lin")
		urllib.request.urlretrieve(url, local_path)
	elif plataforma == "Darwin":
		print("Espere mientras se descarga chromedriver")
		url = get_chromedriver_url()
		makdirect("dar")
		urllib.request.urlretrieve(url, local_path)
	else:
		print("Error")

	with ZipFile(local_path, 'r') as desc:
		desc.extractall('bin')

	if os.path.exists(local_path):
		os.remove(local_path)
	else:
		print("el archivo ya ha sido borrado")

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