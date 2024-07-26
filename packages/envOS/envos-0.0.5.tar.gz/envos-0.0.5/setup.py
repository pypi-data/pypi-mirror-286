import pathlib
from setuptools import find_packages, setup

with open('./README.md', 'r', encoding='utf-8') as fh:
  readme = fh.read()

setup(
  name='envOS',
  version='0.0.5',
  description='Obtiene las variables de entorno, para tener mantenimientos eficientes',
  long_description=readme,
  long_description_content_type='text/markdown',
  author='Pedro Jesús Pérez Hernández',
  author_email='pedrojesus.perez@welldex.mx',
  url='https://gitwell.gwldx.com:2443/python_libraries/envOS.git',
  install_requires=[],
  license='MIT',
  packages=find_packages(),
  include_package_data=True
)