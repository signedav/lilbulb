import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lilbulb",
    version="1.0.1",
    author="Dave Signer",
    author_email="david@opengis.ch",
    description="Dave's lil' bulb - small function lib for creating ilidata.xml files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/signedav/lilbulb",
    classifiers=[
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['lilbulb'],
    python_requires=">=3.6",
)