from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='sophi-app-internal',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyjwt',
        'cryptography',
        'python-jose',
        'pydantic',
        'azure-cosmos'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)