from setuptools import setup, find_packages

setup(
    name="doc-scanner",
    version="0.5",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    description="A script to scan HTML documents for forbidden phrases stored in a CSV.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Marcin Walczak",
    url="https://github.com/marcinwalczak2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'requests',
        'pandas',
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'docscanner=docscanner.docscanner:main',
        ],
    },
    package_data={
        'docscanner': ['data/Style Guide Phrases.csv'],
    },
)