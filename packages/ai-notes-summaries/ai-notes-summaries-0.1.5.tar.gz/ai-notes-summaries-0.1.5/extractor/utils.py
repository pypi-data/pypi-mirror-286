from uuid import uuid4
from typing import TypedDict, Literal
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from extractor.models import SampleExtraction


class OpenAIFunctionCallFunctionFieldDef(TypedDict):
    name: str
    arguments: str


class OpenAIFunctionCallDef(TypedDict):
    id: str
    type: Literal["function"]
    function: OpenAIFunctionCallFunctionFieldDef


def get_messages_from_example(example: SampleExtraction) -> list[BaseMessage]:
    """
    Converts an example note into a list of messages that can be fed into an LLM.

    The conversion is as follows:
    - "input": transformed into a single `HumanMessage` object
    - "extracted_notes": transformed into a list of dictionaries that define tool calls for an `AIMessage` object
    """
    messages = [HumanMessage(content=example["input"])]

    tool_calls: list[OpenAIFunctionCallDef] = []
    for extracted_note in example["extracted_notes"].notes:
        tool_calls.append(
            {
                "id": str(uuid4()),
                "type": "function",
                "function": {
                    # for now langchain accepts the name of the pydantic model as the name of the function
                    "name": extracted_note.__class__.__name__,
                    "arguments": extracted_note.json(),
                },
            }
        )

    messages.append(AIMessage(content="", additional_kwargs={"tool_calls": tool_calls}))

    # append ToolMessages to make sure the LLM gets feedback on the result of the function calls
    tool_message_texts = ["You have called the function correctly."] * len(tool_calls)
    messages.extend(
        ToolMessage(content=msg_text, tool_call_id=tool_call["id"])
        for msg_text, tool_call in zip(tool_message_texts, tool_calls)
    )

    return messages


def get_sample_as_input(file_name: str) -> str:
    with open((f"extractor/examples/{file_name}.txt"), "r") as file:
        return file.read()
