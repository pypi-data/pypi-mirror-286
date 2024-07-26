from setuptools import setup, find_packages

setup(
    name='drcode-wrapper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'sentry-sdk',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A wrapper for Sentry SDK initialization',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/drcode-wrapper-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)