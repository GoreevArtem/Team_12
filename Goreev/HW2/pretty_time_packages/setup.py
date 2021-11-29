from setuptools import setup

setup(
    name='pretty_time_packages',
    version='0.1',
    description='gets unixtime in datetime format',
    url='https://github.com/GoreevArtem/Team_12',
    author='Goreev Artoym',
    author_email='artiom.goreev@yandex.ru',
    license='MIT',
    namespace_packages=['get_pretty_time_package'],
    packages=['get_pretty_time_package'],
    entry_points={
        'console_scripts': [
            'get_time_pp=get_pretty_time_package.pretty_print_module:main',
        ]
    }
)
