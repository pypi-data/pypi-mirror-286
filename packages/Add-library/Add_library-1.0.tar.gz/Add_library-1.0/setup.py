from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='Add_library',
    version='1.0',
    author='Dr_Andreiika',
    author_email='sedunovandrey2007@gmail.com',
    description='This is the simplest module for add two numbers',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/FessLeru/',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='Add ',
    project_urls={
        'GitHub': 'https://github.com/FessLeru/'
    },
    python_requires='>=3.6'
)
