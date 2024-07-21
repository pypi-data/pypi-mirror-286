from setuptools import setup

setup(
    name='my_swiki',
    version='10.1.1',
    description='A program for searching and reading Wikipedia articles in multiple languages',
    py_modules=['my_swiki'],
    author='k0ng999',
    author_email='baydar_14@mail.ru',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)
