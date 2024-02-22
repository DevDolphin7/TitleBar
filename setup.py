from setuptools import setup

setup(
    name='TitleBarCTk',
    version='0.1.1',
    install_requires=[
        'pywin32',
        'screeninfo',
        'pillow',
        'customtkinter',
    ],
    description="Create a custom title bar for a windows app developed with custom tkinter",
    long_description="""pip install TitleBarCTk

Create a custom title bar for a windows app developed with custom tkinter.

For futher information go to: https://github.com/DevDolphin7/TitleBar
Or get in contact at DevDolphin7@outlook.com"""
)
