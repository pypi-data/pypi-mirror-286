from setuptools import setup, find_packages
import os

README = os.path.join(os.path.dirname(__file__), 'README.md')
with open(README, 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="hyperprotocols", 
    version="0.0.5",
    author="Joel Yisrael", 
    author_email="joel@sss.bot", 
    description="simple tools for advanced web related actions", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schizoprada/hyperprotocols", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)