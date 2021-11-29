from setuptools import setup

setup(
    name='pretty_print_package',
    version='0.1',
    description='description',
    url='http://github.com/name/package_name',
    author='Your Name',
    author_email='email@example.com',
    license='MIT',
    namespace_packages=['get_time'],
    packages=['get_time.pretty_print_package'],
    install_requires=[
        'requests==2.26.0',
        'get_time_package'
    ],

    entry_points={
        'console_scripts': [
            'get_time_pp=get_time.pretty_print_package.pretty_print_module:main'
        ]
    },
    zip_safe=False
)
