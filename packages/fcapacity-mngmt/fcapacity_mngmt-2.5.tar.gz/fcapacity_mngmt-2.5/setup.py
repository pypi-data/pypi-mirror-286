from setuptools import setup, find_packages

setup(
    name="fcapacity_mngmt",
    version="2.5",
    author="Jorge Marmol",
    author_email="marmoljorge98@gmail.com",
    packages=find_packages(),
    install_requires=["azure-identity","azure-mgmt-resource"],  # Agrega las dependencias si las tienes
)


# python setup.py sdist
