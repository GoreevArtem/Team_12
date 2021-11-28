from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='get_time_package',
    version='0.1',
    description='description',
    url='http://github.com/name/package_name',
    author='Your Name',
    author_email='email@example.com',
    license='MIT',
    namespace_packages=['get_time_packages_project'],
    packages=['get_time_packages_project.get_time_package'],
    install_requires=[
        'requests==2.26.0',
    ],
    entry_points={
        'console_scripts': [
            'get_time=get_time_packages_project.get_time_package.get_time_module:main'
        ]
    },
    zip_safe=False
)
