import setuptools


with open("README.md", "r") as f:
    long_describe = f.read()


setuptools.setup(
    name="test_build_pypi",
    version="0.0.1",
    author="hiyoung",
    author_email="hiyoungliu@gmail.com",
    description="测试 build pypi",
    long_description=long_describe,
    long_description_content_type="text/markdown",
    url="https://github.com/hiyoung123",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)