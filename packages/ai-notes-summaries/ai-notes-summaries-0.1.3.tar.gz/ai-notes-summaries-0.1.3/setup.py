from setuptools import setup, find_packages


# Function to read the requirements.txt file
def read_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="ai-notes-summaries",
    version="0.1.3",
    packages=find_packages(),
    install_requires=read_requirements(),
    url="https://github.com/CodeWithOz/ai-notes-summaries",
    author="Uche Ozoemena",
    author_email="codewithoz@outlook.com",
    description="An AI-powered tool that extracts structured notes from a given piece of text.",
)
