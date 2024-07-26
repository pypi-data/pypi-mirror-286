from setuptools import setup, find_packages

setup(
    name="modelhub-sdk",
    version="0.1.2",
    description="SDK for ModelHub to create and manage machine learning pipelines",
    author="Jagveer Singh",
    author_email="jagveer@autonomize.ai",
    url="https://github.com/yourusername/modelhub-sdk",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "pyyaml",
        "jinja2",
        "kubernetes",
        "requests",
        "aiohttp",
        "mlflow",
        "azure-storage-blob",
        "azure-identity",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
