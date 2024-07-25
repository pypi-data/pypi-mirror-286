from setuptools import setup, find_packages

setup(
    name='python_selenium_google_form',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'undetected_chromedriver==3.5.5',
        'selenium==4.22.0'
    ],
)
