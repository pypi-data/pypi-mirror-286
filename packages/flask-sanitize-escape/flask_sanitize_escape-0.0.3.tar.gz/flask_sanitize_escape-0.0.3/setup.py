# setup.py

from setuptools import setup

setup(
    name='flask-sanitize-escape',
    version='0.0.3',
    description='Sanitization functions for Flask backend input to prevent XSS, RCE, SQLi and many others',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mayur19/flask-sanitize-escape',
    author='Mayur Dusane',
    author_email='mayurdusane1@gmail.com',
    packages=['flask_sanitize_escape'],
    install_requires=[
        'Flask',
    ],
    classifiers=[  # Optional classifiers for PyPI categorization
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
