from setuptools import setup
import os
from pathlib import Path
import time

readme = open(f'./readme.md').read()

setup(
    name='IoT Deployment Generator',
    version='0.0.14',
    description='Library used to create Azure IoT Edge deployment templates with python code ',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='iot edge azure',
    license='MIT License',
    author='Shoter',
    url='https://github.com/shoter/IotDeploymentGenerator',
    packages=[
        'IDG',
        'IDG.exceptions'
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)