from setuptools import find_packages, setup


with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="data-quality-kit",
    version="0.0.1",
    description=" library of functions for managing and improving data quality in Datasets",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dante33CTP/data-quality-kit",
    author="DantePedrozo",
    author_email="dante.victor.33@gmail.com",
    license="Apache License 2.0",
    keywords="Data Quality",
    install_requires=["pandas >= 2.2.2", "assertpy >= 1.1.0 ", "pytest >= 8.2.2"],
    test_suite='tests',
    tests_require=['pytest'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]

)
