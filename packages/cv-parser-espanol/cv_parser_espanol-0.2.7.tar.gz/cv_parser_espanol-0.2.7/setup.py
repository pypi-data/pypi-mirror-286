from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cv_parser_espanol',
    version='0.2.7',
    packages=find_packages(),
    install_requires=[
        'spacy',
        'PyMuPDF'
    ],
    entry_points={
        'console_scripts': [
            # Si quieres agregar scripts ejecutables
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',  
)