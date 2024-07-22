
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chzzk",
    version="0.1",
    author="Allen_Lee",
    author_email="paranelf66@gmail.com",
    description="Check whether the user's data is a URL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.kwserver.store",
    project_urls={
        "Bug Tracker": "https://www.kwserver.store",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)