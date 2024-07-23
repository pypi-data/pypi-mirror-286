from setuptools import setup, find_packages

setup(
    name='driverApi',
    version='1.0.0',
    packages=find_packages(),
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
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        # Add more classifiers as needed
    ],
)
