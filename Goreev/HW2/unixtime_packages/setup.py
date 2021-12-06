from setuptools import setup

setup(
    name='unixtime_package',
    version='0.1',
    description='gets unixtime',
    url='https://github.com/GoreevArtem/Team_12',
    author='Goreev Artoym',
    author_email='artiom.goreev@yandex.ru',
    license='MIT',
    namespace_packages=['get_unixtime_package'],
    packages=['get_unixtime_package'],
    install_requires=[
        'requests==2.26.0',
    ],
    entry_points={
        'console_scripts': [
            'get_time=get_unixtime_package.get_unixtime_module:main',
        ]
    }
)
