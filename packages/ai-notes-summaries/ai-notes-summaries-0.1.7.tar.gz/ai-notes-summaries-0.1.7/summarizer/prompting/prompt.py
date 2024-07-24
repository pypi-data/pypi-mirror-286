from langchain_core.prompts import ChatPromptTemplate
import os


def get_summarizer_prompt():
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "summarizer.txt"
    )
    with open(file_path, "r") as file:
        prompt = file.read()

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                prompt,
            ),
            ("human", "{text}"),
        ]
    )
