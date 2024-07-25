from setuptools import setup, find_packages

setup(
    name="redis_management",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "redis",  # Specify the Minimum Version if Necessary
        "python-decouple",
        "cryptography==42.0.8"
    ],
    include_package_data=True,
    description="A utility package for managing Redis keys.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AAbbasRR/redis-manager.git",
    author="Abbas Rahimzadeh",
    author_email="arahimzadeh79@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
