from setuptools import setup, find_packages


def readme():
  with open('docs.md', 'r') as f:
    return f.read()


setup(
  name='telegram_webapps_authentication',
  version='1.0.1',
  author='Danila Dudin',
  author_email='sten1243@gmail.com',
  description='This Python package provides an authentication mechanism for Telegram web apps. It implements the algorithm for validating data received from a Telegram web app, ensuring the authenticity and integrity of the data.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/danyadanyaa/telegram_webapps_authentication',
  packages=find_packages(),
  install_requires=['pydantic~=2.8.2'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='telegram webapp webapps auth authentication ',
  project_urls={
    'GitHub': 'https://github.com/danyadanyaa',
    'Telegram': 'https://t.me/yadaehodaice'
  },
  python_requires='>=3.6'
)