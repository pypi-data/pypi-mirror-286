from setuptools import setup

def readme():
    with open('README.md', 'r') as file:
        file.read()

setup(name='florestdevtools', version='0.0.1-alpha', description='Личная библиотека Флореста, написанная на Python.', long_description=readme(), long_description_content_type='text/markdown', packages=['florestdevtools'], author='florestdev4185', author_email='florestone4185@internet.ru', requires=['discord', 'g4f', 'MukeshAPI', 'pypresence', 'curl_cffi'])