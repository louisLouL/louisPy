import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redis_decorator",
    version="0.3",
    author="Louis Lou",
    author_email="qijia.lou@nyu.edu",
    description="Using redis as external redis_dec by one line of code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/louisLouL/louisPy",
    packages=setuptools.find_packages(),
    install_requires=['redis>=2.10.6',
                      'pandas>=0.23.0'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)