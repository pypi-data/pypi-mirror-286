# setup.py
from setuptools import setup, find_packages

setup(
    name="testjson2",
    version="0.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library that runs a script upon installation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="http://example.com/my_library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'run_my_script = my_script:main',
        ],
    },
)
