from setuptools import setup, find_packages

setup(
    name='cv_parser_espanol',
    version='0.1',
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
)