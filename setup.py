from setuptools import setup, find_packages


version = '0.3.0.2'

setup(
    name='django_pony_forms',
    version=version,
    license='Apache License, Version 2.0',
    description='Django pony forms',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['django'],
    author='Marco Braak',
    author_email='mbraak@ridethepony.nl',
    url='https://github.com/mbraak/django_pony_forms',
    download_url='https://github.com/mbraak/django_pony_forms/zipball/master',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
