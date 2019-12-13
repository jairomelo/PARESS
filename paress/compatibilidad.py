import os
import platform
import sys
import urllib.request
from zipfile import ZipFile

from win32api import GetFileVersionInfo
from win32api import HIWORD
from win32api import LOWORD

'''
Obtener la versión de Chrome
'''


def win_get_version_number(filename):
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
    except:
        return "Unknown version"


def versionplat():
    if sys.platform.startswith('win'):
        try:
            versionpre = ".".join([str(i) for i in win_get_version_number(
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')])
        except:
            versionpre = ".".join([str(i) for i in win_get_version_number(
                r'C:\Program Files\Google\Chrome\Application\chrome.exe')])
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        versionpre = input("Ingrese la versión Chrome que tenga instalada: ")

    return versionpre[:2]


def chversion(versionlocal=versionplat()):
    if versionlocal == "77":
        chversion = "77.0.3865.40"
    elif versionlocal == "78":
        chversion = "78.0.3904.105"
    elif versionlocal == "79":
        chversion = "79.0.3945.36"
    elif versionlocal == "76":
        chversion = "76.0.3809.68"
    else:
        print("Su versión de Chrome es 75 o menor. Puede actualizarla a una versión superior e intente nuevamente.")

    return chversion


plataforma = platform.system()
local_path = 'bin/chromedriver.zip'


def get_chromedriver_url(version=chversion()):
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

    try:
        os.remove(local_path)
    except:
        print("el archivo ya ha sido borrado")
