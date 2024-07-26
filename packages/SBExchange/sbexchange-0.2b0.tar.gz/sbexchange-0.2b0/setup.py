from setuptools import setup, find_packages

with open("README.md", "r") as f:
  description= f.read()
setup(
  name="SBExchange",
  version="0.2Beta",
  install_requires=[
  ],
  long_description=description,
  long_description_content_type="text/markdown"
)