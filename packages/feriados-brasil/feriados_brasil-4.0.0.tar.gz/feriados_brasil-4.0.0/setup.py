from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='feriados_brasil',
    version='4.0.0',
    license='MIT License',
    author='Luiz Fernando T. Rodrigues',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='euluizfernando2001@gmail.com',
    keywords='feriados br',
    description=u'Versão beta não oficial de testes',
    packages=['feriado_teste'],
    install_requires=['datetime'],)