from setuptools import setup, find_packages

setup(
    name="humanagent",
    version="0.1.0",
    description="Human checkpoint infrastructure for AI workflows",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Simon Sliman Du Sable",
    url="https://humanagent.net",
    project_urls={
        "Repository": "https://github.com/SimonSliman/humanagent-python",
    },
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
