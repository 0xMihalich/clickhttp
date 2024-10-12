import shutil
from setuptools import setup, find_packages
import pathlib
import pkg_resources


shutil.rmtree("build", ignore_errors=True,)
shutil.rmtree("clickhttp.egg-info", ignore_errors=True,)


with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with open(file="README.md", mode="r", encoding="utf-8",) as f:
    long_description = f.read()

setup(name="clickhttp",
      version="0.0.8",
      packages=find_packages(),
      install_requires=install_requires,
      author="0xMihalich",
      author_email="bayanmobile87@gmail.com",
      description="Работа с БД Clickhouse по HTTP-протоколу",
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False,)
