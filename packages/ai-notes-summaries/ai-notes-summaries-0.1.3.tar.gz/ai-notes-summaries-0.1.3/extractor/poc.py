import uuid
from typing import Optional, TypedDict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, ToolMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
import dotenv

dotenv.load_dotenv()


class Person(BaseModel):
    """Information about a person."""

    # NOTE: that doc string is actually sent to the LLM, so I need to use it wisely to describe what the model represents.

    # NOTE: for the fields:
    # - typing a string as optional allows the model to decline to extract it
    # - the description field is used by the model, so adding it can improve extraction results
    name: Optional[str] = Field(default=None, description="The name of the person")
    hair_color: Optional[str] = Field(
        default=None, description="The color of the person's hair, if known"
    )
    height_in_meters: Optional[str] = Field(
        default=None, description="Height measured in meters"
    )


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute you're asked to extract, "
            "return null for the attribute's value.",
        ),
        MessagesPlaceholder("examples"),
        ("human", "{text}"),
    ]
)


def get_open_ai_runnable(schema_klass):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    return prompt | llm.with_structured_output(schema=schema_klass)


def get_mistral_ai_runnable(schema_klass):
    llm = ChatMistralAI(model="mistral-large-latest", temperature=0)

    return prompt | llm.with_structured_output(schema=schema_klass)


text = "Alan Smith is 6 feet tall and has blond hair."
# res = get_open_ai_runnable(schema_klass=Person).invoke({"text": text})
# res = get_open_ai_runnable(schema_klass=Person).invoke({"text": text})


class Data(BaseModel):
    """Extracted data about people"""

    people: list[Person]


# runnable = get_open_ai_runnable(schema_klass=Data).invoke(
#     {
#         "text": "My name is Jeff, my hair is black and i am 6 feet tall. Anna has the same color hair as me."
#     }
# )


class Example(TypedDict):
    """
    A representation of an example consisting of the text input, expected tool calls, and optionally the tool call results.

    For extraction tasks, the tool calls are represented as instances of the Pydantic BaseModel and the tool call results can be simply sentences telling the model that it called the tool correctly.
    """

    input: str
    tool_calls: list[BaseModel]
    tool_call_responses: Optional[list[str]]


def tool_example_to_messages(example: Example) -> list[BaseMessage]:
    """
    Converts an example into messages that can be fed into the model.

    For each example this function will output 3 types of messages:
    (1) HumanMessage: input text from which content should be extracted
    (2) AIMessage: sample response from the LLM that will contain tool call definition(s)
    (3) ToolMessage: sample response back to the LLM to confirm that its tool call definitions were correct
    """
    # first specify the human message
    messages: list[BaseMessage] = [HumanMessage(content=example["input"])]

    # then prepare the tool call definitions for the AI message
    openai_tool_calls = []
    for tool_call in example["tool_calls"]:
        openai_tool_calls.append(
            {
                "id": str(uuid.uuid4()),
                "type": "function",
                "function": {
                    # for now the name of the function is the name of the pydantic
                    # model class that we want to see in the output
                    "name": tool_call.__class__.__name__,
                    "arguments": tool_call.json(),
                },
            }
        )
    # then specify the AI message using those definitions
    messages.append(
        AIMessage(content="", additional_kwargs={"tool_calls": openai_tool_calls})
    )
    # then specify the tool message
    tool_call_responses = example.get("tool_call_responses") or [
        "You have correctly called this tool."
    ] * len(openai_tool_calls)
    # each tool call response must be mapped to the ID of its corresponding tool call definition
    messages.extend(
        ToolMessage(content=response, tool_call_id=tool_call["id"])
        for response, tool_call in zip(tool_call_responses, openai_tool_calls)
    )

    return messages


examples = [
    (
        "The ocean is vast and blue. It's more than 20,000 feet deep. There are many fish in it.",
        Person(name=None, hair_color=None, height_in_meters=None),
    ),
    (
        "Fiona traveled far from France to Spain.",
        Person(name="Fiona", hair_color=None, height_in_meters=None),
    ),
]

messages = []
for text, extracted_person in examples:
    messages.extend(
        tool_example_to_messages(Example(input=text, tool_calls=[extracted_person]))
    )

res = prompt.invoke({"text": "this is some text", "examples": messages})


def get_open_ai_extractor(schema_klass):
    llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)

    return prompt | llm.with_structured_output(schema=schema_klass, include_raw=False)


print("========= without examples =========")
for _i in range(5):
    text = "The solar system is large, but earth has only 1 moon."
    print(get_open_ai_extractor(Person).invoke({"text": text, "examples": []}))

print("========= with examples =========")
for _i in range(5):
    text = "The solar system is large, but earth has only 1 moon."
    print(get_open_ai_extractor(Person).invoke({"text": text, "examples": messages}))
