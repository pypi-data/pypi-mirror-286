import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kblpbyp",
    version="1.0.1",
    author="JeongJun Moon",
    author_email="jaymnetwork@gmail.com",
    url="https://jaymnetwork.github.io/jeongjunemoon/",
    description="Web scraping and visualization tools for Korean Basketball League's play-by-play data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
