from setuptools import setup, find_packages


version = '0.6.0'

setup(
    name='django_pony_forms',
    version=version,
    license='Apache License, Version 2.0',
    description='Django-pony-forms helps you to write better html for your Django forms',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'backports.functools_lru_cache',
        'six'
    ],
    author='Marco Braak',
    author_email='mbraak@ridethepony.nl',
    url='https://github.com/mbraak/django_pony_forms',
    download_url='https://github.com/mbraak/django_pony_forms/zipball/master',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ]
)
