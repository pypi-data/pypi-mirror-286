from setuptools import setup, find_packages

setup(
    name='YtDuration',
    version='0.1',
    description='A Python package to get the duration of a YouTube video without using the YouTube Data API.',
    author='Ranjit',
    author_email='ranjitmaity95@gmail.com',
    url='https://github.com/RanjitM007/YtDuration',  # Replace with your GitHub repository URL
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
