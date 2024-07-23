from setuptools import setup, find_packages


with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="textg2p",
    version="0.1.5",
    author="Ivan Shivalov",
    author_email="ivansivalov396@gmail.com",
    url="https://github.com/intexcor/textg2p",
    description="A package to transform texts to ipa",
    package_dir={'textg2p': 'textg2p'},
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["eng-to-ipa", "epitran", "jamo", "g2pk", "lingua-language-detector"],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
