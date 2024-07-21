from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='simple_sock',
    version='0.1.3',
    author='Leonardo Oliveira',
    author_email='lo570354@gmail.com',
    description='A Python library for simplified network and HTTP connections management.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    keywords=["simplified", "socket", "simple", "sock", "network", "easy"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=[],
)
