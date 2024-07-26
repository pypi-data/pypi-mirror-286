from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='python_selenium_google_form',
    version='0.5.0',
    packages=find_packages(),
    install_requires=[
        'undetected_chromedriver==3.5.5',
        'selenium==4.23.1',
        'setuptools==71.1.0'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
