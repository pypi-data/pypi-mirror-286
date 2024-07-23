from setuptools import setup, find_packages

setup(
    name="pyf_login",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "djangorestframework",
        "PyJWT",
    ],
    include_package_data=True,
    description="A reusable Django login package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    author="ycx",
    author_email="ycx3030@126.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
