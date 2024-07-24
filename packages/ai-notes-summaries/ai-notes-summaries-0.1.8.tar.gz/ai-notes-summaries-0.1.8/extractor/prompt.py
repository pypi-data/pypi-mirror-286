from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_extractor_prompt_template():
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert extraction algorithm. "
                "You are to extract key themes, lessons, and potential action items from the text. "
                "If you do not know the value of an attribute you're asked to extract, "
                "return null for the attribute's value.",
            ),
            MessagesPlaceholder("examples"),
            ("human", "{text}"),
        ]
    )

    return prompt_template
