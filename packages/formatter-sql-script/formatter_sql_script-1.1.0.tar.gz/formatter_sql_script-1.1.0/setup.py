from setuptools import find_packages, setup

readme = open('./README.md', 'r')

setup(
    name='formatter_sql_script',
    version='1.1.0',
    description='Formateador de texto a sentencia de SQL (Insert y Update)',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Felipe Medel',
    author_email='luispipemedel@gmail.com',
    packages=find_packages(),
    py_modules=['formatter_sql_script'],
    keywords=['helper', 'sql Formatter', 'testing', 'dev'],
    license='MIT',
    include_package_data=True
)