from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="component_reuse",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here
    ],
    entry_points={
        "console_scripts": ["Component_Reuse = Component_Reuse:hello"],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
