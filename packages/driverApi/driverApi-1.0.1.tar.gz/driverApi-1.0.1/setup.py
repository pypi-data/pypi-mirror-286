from setuptools import find_packages, setup

setup(
    name='driverApi',
    version='1.0.1',

    # packages=find_packages(exclude=['common', 'control/*', 'view/*'], include=['device', 'logger', 'driver']),
    # packages=find_packages(
    #     exclude=['common', 'control', 'driver', 'exception', 'service_adpter', 'model', 'spi', 'task', 'view',
    #              'webservice']),
    packages=find_packages(include=['device', 'device.*', 'driverApi', 'logger']),
    py_modules=['common.singleton', 'common.global_constants'],
    install_requires=[
        # List dependencies here if your package requires any
    ],
    entry_points={
        # Optional: Define entry points here if your package provides any command-line scripts
    },
    # Optional: Metadata about your package
    author='maoshiman',
    author_email='shiman.mao@gientech.com',
    description='外设驱动接口',
    long_description='外设驱动实现接口的基本定义',
    long_description_content_type='text/markdown',
    classifiers=[
    ],
)
