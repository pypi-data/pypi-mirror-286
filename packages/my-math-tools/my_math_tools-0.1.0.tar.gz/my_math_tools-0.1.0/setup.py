# setup.py

from setuptools import setup, find_packages

setup(
    name='my_math_tools',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Jinglin Zhao',
    author_email='jinglinzhao@gmail.com',
    description='A simple math tools library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_math_tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
