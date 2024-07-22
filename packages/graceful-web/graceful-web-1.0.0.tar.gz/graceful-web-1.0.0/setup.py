from setuptools import setup, find_packages


with open("readme.md", "r") as file:
    description = file.read()


setup(
    name="graceful-web",
    version="1.0.0",
    description="A lightweight and efficient web framework",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Nolan M. McAllister",
    author_email="nolan.m.mcallister@gmail.com",
    url="https://github.com/nolanM123/graceful",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.4",
)
