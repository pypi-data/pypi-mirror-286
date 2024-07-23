from setuptools import setup, find_packages

setup(
    name='examplepkg0512',
    version='0.1',
    author='MG',
    author_email='porwalmohit789@gmail.com',
    description='A simple example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mohitgupta2021/examplepkg',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
