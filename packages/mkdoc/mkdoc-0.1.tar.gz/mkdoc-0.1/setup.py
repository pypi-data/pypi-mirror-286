from setuptools import setup, find_packages

setup(
    name="mkdoc",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "mkdoc=mkdoc.mkdoc:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for generating Markdown documentation from image directories",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mkdoc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
