from setuptools import find_packages
from distutils.core import setup

setup(name="ICQBot",
      version = "0.0.1-alpha",
      author="Kamuri Amorim",
      author_email='luiz.k.amorim@gmail.com',
      url="https://github.com/kamuridesu/ICQBotPy",
      download_url = "https://github.com/kamuridesu/ICQBotPy.git",
      long_description="""ICQ bot framework""",
      license="MIT",
      packages=find_packages("."),
      install_requires=[
        'requests'
      ]

)
