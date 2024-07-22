from setuptools import setup, find_packages

setup(
    name='azizitc',
    version='0.1.0',
    packages=find_packages(),
    description='A simple package for changing text color in terminal.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/Azizi030/textcolor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)