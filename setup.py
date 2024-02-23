from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.txt").read_text()

setup(
    name='titlebarctk',
    version='0.1.2',
    install_requires=[
        'pywin32',
        'screeninfo',
        'pillow',
        'customtkinter',
    ],
    long_description=long_description,
    long_description_content_type="text/plain"
)
