from setuptools import setup, find_packages

with open("README.md", "r") as f:
  description= f.read()
setup(
  name="SBExchange",
  version="0.21",
  install_requires=[
  ],
  long_description=description,
  long_description_content_type="text/markdown"
)