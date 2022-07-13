from setuptools import find_packages
from distutils.core import setup


def description():
  with open("README.md", "r") as f:
    return f.read()


def requirements():
  with open("requirements.txt", "r") as f:
    return f.read().split("\n")


setup(name="ICQBot",
      version = "0.2.1-beta",
      author="Kamuri Amorim",
      author_email='luiz.k.amorim@gmail.com',
      url="https://github.com/kamuridesu/ICQBotPy",
      download_url = "https://github.com/kamuridesu/ICQBotPy/archive/refs/heads/main.zip",
      long_description=description(),
      long_description_content_type="text/markdown",
      license="MIT",
      packages=find_packages("."),
      install_requires=requirements()
)
