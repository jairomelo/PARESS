import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
    name="paress",
    version="0.0.12",
    author="Jairo Antonio Melo Flórez",
    author_email="jairom@colmich.edu.mx",
    description="Utilidad para Web Scrapping en el Portal de Archivos Españoles-PARES",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jairomelo/PARESS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)