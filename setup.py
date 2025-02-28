from setuptools import setup, find_packages

setup(
    name="app_dir",
    packages=find_packages(),
    install_requires=[
        "flask==2.0.1",
        "werkzeug==2.0.3",
    ],
)
