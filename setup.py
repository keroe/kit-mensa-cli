import setuptools

with open("README.md", "r", encoding="utf-8") as markdown_description:
    long_description = markdown_description.read()

setuptools.setup(
    name="kit-mensa-cli",
    version="0.0.1",
    author="Kevin Rösch",
    author_email="kevin.roesch@kit.edu",
    description=(
        "A commmand line interface to get the menu of the KIT mensa for the current day."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keroe/kit-mensa-cli",
    project_urls={
        "Bug Tracker": "https://github.com/keroe/kit-mensa-cli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "download = kit_mensa.cli:main",
        ]
    },
)
