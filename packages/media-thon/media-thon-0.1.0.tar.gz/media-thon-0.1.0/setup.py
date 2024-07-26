from setuptools import setup, find_packages

setup(
    name='media-thon',
    version='0.1.0',
    description='A Python library for downloading images from Pinterest',
    author='Amal nath',
    author_email='amalnath0600@gmail.com',
    url="https://github.com/MrTG-CodeBot",
    telegram_url="https://t.me/MrTG_Coder",
    packages=find_packages(),
    install_requires=['requests', 'bs4'],
)
