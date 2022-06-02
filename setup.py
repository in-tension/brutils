from setuptools import setup

setup(
    name='brutils',
    version='0.1dev',
    packages=['brutils',],
    license='WTFPL',

    install_requires=[
        'numpy',
        'altair',
        'matplotlib']
    # long_description=open('README.txt').read(),
)
