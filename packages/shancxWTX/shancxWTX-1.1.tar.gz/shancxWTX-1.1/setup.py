from setuptools import setup, find_packages

setup(
    name='shancxWTX',
    version='1.01',
    packages=find_packages(),
    description='A simple timer decorator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='shanchangxi',
    author_email='shanhe12@163.com',
    url='https://github.com/shanchanghua',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)