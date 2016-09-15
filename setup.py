from distutils.core import setup

setup(
    name='bottle-filters',
    version='0.1',
    packages=['bottle_smart_filters'],
    url='https://github.com/agile4you/bottle-smart-filters',
    license='GLPv3',
    author='pav',
    author_email='vpapavasil@gmail.com',
    description='Bottle.py QueryString Params consistent handling.',
    extras_require={
        'test': ['pytest', 'bottle', 'six'],
    }
)
