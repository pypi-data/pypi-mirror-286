from setuptools import setup, find_packages

setup(
    name="modelhub_autonomize",
    version="0.1.0",
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
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)