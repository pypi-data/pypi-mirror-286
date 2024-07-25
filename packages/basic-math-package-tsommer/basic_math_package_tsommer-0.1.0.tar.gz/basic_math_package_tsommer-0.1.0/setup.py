import setuptools

with open("README.md", "r") as f:
  long_description = f.read()

setuptools.setup(
  name = "basic_math_package_tsommer",
  version = "0.1.0",
  author = "TAMAR",
  author_email = "tzirw@example.com",
  description= "A basic math package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(where='src'),
  package_dir={"":"src"},
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  pythom_requires=">=3.8.0",
)