from setuptools import setup, find_packages

setup(
    name="archbyte",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Arch Byte",
    author_email="cophtew@gmail.com",
    description="Arch Byte library",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/archbyte",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
