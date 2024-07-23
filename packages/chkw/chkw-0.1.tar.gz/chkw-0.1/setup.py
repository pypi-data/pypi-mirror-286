from setuptools import setup, find_packages

setup(
    name='chkw',
    version='0.1',
    py_modules=['chkw'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        chkw=chkw:cli
    ''',
)