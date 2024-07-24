from setuptools import setup, find_packages

REQUIRED_PACKAGES = [
    'jjsystem>=1.0.0,<2.0.0',
    'flask-cors'
]

setup(
    name="jjlocal",
    version="1.0.0",
    summary='JJLocal Module Framework',
    description="JJLocal backend Flask REST service",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES
)
