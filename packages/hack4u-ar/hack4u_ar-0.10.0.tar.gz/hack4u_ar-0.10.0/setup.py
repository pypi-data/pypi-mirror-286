from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u_ar",
    version="0.10.0",
    packages=find_packages(),
    install_requires=[],
    author="Aridany Suárez",
    description="una biblioteca para consultar Hack4u.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io", 
)





