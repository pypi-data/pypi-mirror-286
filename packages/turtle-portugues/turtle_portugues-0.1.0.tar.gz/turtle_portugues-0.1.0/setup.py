from setuptools import setup, find_packages

setup(
    name="turtle_portugues",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Vinicius Hissayoshi Nishida",
    author_email="viniciusnishida13@gmail.com",
    description="Uma biblioteca turtle traduzida para o português.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/viniHNS/Tartaruga_Python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
