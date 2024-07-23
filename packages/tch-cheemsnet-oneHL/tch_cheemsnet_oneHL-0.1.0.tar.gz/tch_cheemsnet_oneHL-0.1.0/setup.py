# setup.py
from setuptools import setup, find_packages

setup(
    name='tch_cheemsnet_oneHL',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0.0',
    ],
    author='Subhodeep Moitra, Deblina Banerjee, Dr. Pintu Pal',
    author_email='subhodeep2000@gmail.com, banerjeedeblina07@gmail.com, dr.ppal.aec@gmail.com',
    description='A custom model for tabular data using attention and feature transformer blocks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/subhodeepmoitra/CheemsNet-one-layer',  # Replace with your GitHub repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
