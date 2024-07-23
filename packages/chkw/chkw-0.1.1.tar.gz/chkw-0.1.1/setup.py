from setuptools import setup, find_packages

setup(
    name='chkw',
    version='0.1.1',
    py_modules=['main'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        chkw=main:cli
    ''',
)