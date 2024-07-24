from setuptools import setup, find_packages

setup(
    name="app_de_tenismiguel",
    version="5.0",
    description="Esta es mi primera prueba para pypi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Miguel Zamit",
    author_email="tenis@gmail.com",
    url="https://google.com", # Se puede poner la url de un repositorio de github
    license_files=["LICENSE"],
    packages=find_packages(),

    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python"
    ]

)