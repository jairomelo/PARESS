import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="paress",
    version="0.0.147",
    author="Jairo Antonio Melo Flórez",
    author_email="jairom@colmich.edu.mx",
    description="Utilidad para Web Scrapping en el Portal de Archivos Españoles-PARES",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jairomelo/PARESS",
    packages=setuptools.find_packages(),
    install_requires=['selenium','beautifulsoup4','requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
