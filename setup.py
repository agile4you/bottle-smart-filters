from distutils.core import setup
import re
import ast


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('bottle_smart_filters/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))


setup(
    name='bottle-smart-filters',
    version=version,
    packages=['bottle_smart_filters'],
    url='https://github.com/agile4you/bottle-smart-filters',
    license='GLPv3',
    author='pav',
    author_email='vpapavasil@gmail.com',
    description='Bottle.py QueryString Params smart guessing.',
    install_requires=[
        'pytest', 'bottle', 'ujson', 'webtest'
    ]
)
