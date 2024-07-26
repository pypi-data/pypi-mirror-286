from setuptools import setup, find_packages

setup(
    name="intellisys",
    version="0.1.6",  # Make sure this matches the version in intellisys/__init__.py
    packages=find_packages(),
    install_requires=[
        "openai",
        "litellm",
        "jinja2",
        "onepasswordconnectsdk",
    ],
    author="Mark Powers",
    author_email="mpoweru@lifsys.com",
    description="Provides intelligence/AI services for the Lifsys Enterprise",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/intellisys",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
