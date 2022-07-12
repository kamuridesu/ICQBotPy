from setuptools import find_packages
from distutils.core import setup

setup(name="ICQBot",
      version = "0.0.5-alpha",
      author="Kamuri Amorim",
      author_email='luiz.k.amorim@gmail.com',
      url="https://github.com/kamuridesu/ICQBotPy",
      download_url = "https://github.com/kamuridesu/ICQBotPy/archive/refs/heads/main.zip",
      long_description="""ICQ bot framework""",
      license="MIT",
      packages=find_packages("."),
      install_requires=[
        'requests'
      ]
)
