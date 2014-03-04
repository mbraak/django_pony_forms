from setuptools import setup, find_packages


version = '0.3.5.2'

setup(
    name='django_pony_forms',
    version=version,
    license='Apache License, Version 2.0',
    description='Django-pony-forms helps you to write better html for your Django forms',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django',
        'six'
    ],
    author='Marco Braak',
    author_email='mbraak@ridethepony.nl',
    url='https://github.com/mbraak/django_pony_forms',
    download_url='https://github.com/mbraak/django_pony_forms/zipball/master',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
    ]
)
