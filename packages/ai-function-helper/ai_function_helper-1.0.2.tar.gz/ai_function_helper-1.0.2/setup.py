from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai_function_helper",
    version="1.0.2",
    author="Clad3815",
    author_email="clad3815@gmail.com",
    description="A helper for creating AI-powered functions using OpenAI's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Clad3815/ai-function-helper-python",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "openai",
        "pydantic",
        "jsonschema",
        "colorama",
        "json_repair",
        "pillow",
        "requests",
    ],
)