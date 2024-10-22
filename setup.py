import shutil
from setuptools import setup, find_packages


shutil.rmtree("build", ignore_errors=True,)
shutil.rmtree("clickhttp.egg-info", ignore_errors=True,)

with open(file="README.md", mode="r", encoding="utf-8",) as f:
    long_description = f.read()

long_description += """______________________________________________________________________________________________________________________

"""

with open(file="README_RU.md", mode="r", encoding="utf-8",) as f:
    long_description += f.read()

setup(name="clickhttp",
      version="0.1.2",
      packages=find_packages(),
      author="0xMihalich",
      author_email="bayanmobile87@gmail.com",
      description="Working with Clickhouse Database via HTTP Protocol | Работа с БД Clickhouse по HTTP-протоколу",
      url="https://github.com/0xMihalich/clickhttp",
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False,)
