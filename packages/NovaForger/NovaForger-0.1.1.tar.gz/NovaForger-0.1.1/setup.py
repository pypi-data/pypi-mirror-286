from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NovaForger",
    version="0.1.1",
    author="mizu1",
    author_email="2648307053@qq.com",
    description="A lightweight framework for building LLM applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mizu1/NovaForger",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "aiohttp"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8>=3.9.0",
        ],
    },
)