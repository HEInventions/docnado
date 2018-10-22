from os import environ
from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='docnado',
    version='1.0.2',
    author='Hardy & Ellis Inventions LTD',
    author_email='support@heinventions.com',

    description="A rapid documentation tool to blow you away.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/HEInventions/docnado",

    python_requires='>=3.6.0',

    packages=find_packages(),
    include_package_data=True,
    py_modules=['docnado'],
    install_requires=[
        'Flask==1.0.2',
        'Markdown==2.6.11',
        'timeago==1.0.8',
        'Frozen-Flask==0.15',
        'beautifulsoup4==4.6.3',
        'requests==2.19.1',
        'watchdog==0.9.0',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ),

    entry_points={
        'console_scripts': [
            'docnado = docnado.docnado:main',
        ],
    },
)
