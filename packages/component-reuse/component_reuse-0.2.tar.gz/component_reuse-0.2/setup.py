from setuptools import setup, find_packages

setup(
    name="component_reuse",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here
    ],
    entry_points={
        "console_scripts": ["Component_Reuse = Component_Reuse:hello"],
    },
)
