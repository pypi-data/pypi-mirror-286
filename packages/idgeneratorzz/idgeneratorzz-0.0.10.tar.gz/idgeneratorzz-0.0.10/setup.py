from setuptools import find_packages, setup

with open("idgeneratorzz/README.md", "r") as f:
    long_description = f.read()

setup(
    name="idgeneratorzz",
    version="0.0.10",
    description="An id generator that generated various types and lengths ids",
    package_dir={"": "idgeneratorzz"},
    packages=find_packages(where="idgeneratorzz"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BisaiShanku/python_id_generator",
    author="Shanku Bisai",
    author_email="shankubisai@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson >= 0.5.10"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
