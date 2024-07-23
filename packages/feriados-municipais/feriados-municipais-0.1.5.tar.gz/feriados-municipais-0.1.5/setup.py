from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='feriados-municipais',
    version='0.1.5',
    license='MIT License',
    author='Luiz Fernando Teles Rodrigues',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='euluizfernando2001@gmail.com',
    keywords='feriados br municipais brasil',
    description=u'Versão beta da biblioteca de feriados municipais.',
    packages=['feriados_municipais'],
    install_requires=['datetime'],)