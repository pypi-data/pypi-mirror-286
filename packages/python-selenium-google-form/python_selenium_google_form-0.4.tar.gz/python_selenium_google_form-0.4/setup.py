from setuptools import setup, find_packages

setup(
    name='python_selenium_google_form',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'undetected_chromedriver==3.5.5',
        'selenium==4.23.1',
        'setuptools==71.1.0'
    ],
)
