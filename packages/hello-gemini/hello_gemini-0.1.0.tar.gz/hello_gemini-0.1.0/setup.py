from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description=f.read()

setup(
    name='hello_gemini',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'hello_gemini = hello_gemini:hello_gemini',
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown"
)