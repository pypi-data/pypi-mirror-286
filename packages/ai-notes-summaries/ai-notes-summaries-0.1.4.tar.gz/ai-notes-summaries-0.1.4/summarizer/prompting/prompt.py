from langchain_core.prompts import ChatPromptTemplate


def get_summarizer_prompt():
    with open((f"summarizer/prompting/summarizer.txt"), "r") as file:
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
