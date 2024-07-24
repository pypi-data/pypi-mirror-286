from setuptools import setup, find_packages

setup(
    name="pdfa3extractor",
    version="0.6",
    packages=find_packages(),
    install_requires=[
        "pymupdf",
    ],
    entry_points={
        'console_scripts': [
            'pdfa3extractor=pdfa3extractor.extractor:main',
        ],
    },
    author="PierreGode",
    author_email="pierre@gode.one",
    description="A tool to extract embedded XML files from PDF/A-3 documents",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/PierreGode/pdfa3extractor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
