# email_sender/setup.py
from setuptools import setup, find_packages

setup(
    name='email_sender_zone24x7',
    version='0.1',
    packages=find_packages(),
    install_requires=['secure-smtplib'],
    description='A simple email sending package.',
    author='zone24x7',
    author_email='developer@zone24x7.com',
    url='https://github.com/prasanrzone/email_sender',
)
