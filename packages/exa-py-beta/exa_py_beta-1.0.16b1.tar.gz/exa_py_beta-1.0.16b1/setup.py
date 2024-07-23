from setuptools import setup, find_packages

setup(
    name="exa_py_beta",
    version="1.0.16-beta.1",
    description="[Beta] Python SDK for Exa API.",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    author="Exa",
    author_email="hello@exa.ai",
    package_data={"exa_py_beta": ["py.typed"]},
    url="https://github.com/exa-labs/exa-py-beta",
    packages=find_packages(),
    install_requires=[
        "requests",
        "typing-extensions",
        "openai>=1.10.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Typing :: Typed",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
