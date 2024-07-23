from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='feriados_teste',
    version='5.0.5',
    license='MIT License',
    author='Luiz Fernando T. Rodrigues',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='euluizfernando2001@gmail.com',
    keywords='feriados br',
    description=u'Versão beta não oficial de testes',
    packages=find_packages(),
    install_requires=['datetime'],)