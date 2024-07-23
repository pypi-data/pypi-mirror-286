from setuptools import setup

with open("requirements.txt", encoding="utf-8") as f:
    reqs = f.read().split("\n")

with open("README.md", encoding="utf-8") as f:
    desc = f.read()

setup(
    name="unfolding-vis",
    version="1.0.1",
    author="TimurTimergalin",
    author_email="tmtimergalin8080@gmail.com",
    description="Library for generating thorough web-visualization of Petri nets' unfoldings",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/TimurTimergalin/pn-unfoldings-visualizations",
    packages=["visualize"],
    install_requires=reqs,
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords=["petri-nets unfoldings visualization"]
)
