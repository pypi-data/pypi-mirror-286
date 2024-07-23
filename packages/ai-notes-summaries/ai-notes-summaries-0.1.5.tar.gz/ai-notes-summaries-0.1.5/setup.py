from setuptools import setup, find_packages


setup(
    name="ai-notes-summaries",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "langchain==0.2.6",
        "langchain-openai==0.1.14",
        "langchain-mistralai==0.1.9",
        "python-dotenv==1.0.1",
    ],
    url="https://github.com/CodeWithOz/ai-notes-summaries",
    author="Uche Ozoemena",
    author_email="codewithoz@outlook.com",
    description="An AI-powered tool that extracts structured notes from a given piece of text.",
)
