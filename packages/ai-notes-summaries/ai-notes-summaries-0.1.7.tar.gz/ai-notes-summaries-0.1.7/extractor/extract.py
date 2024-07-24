from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from extractor.models import ExtractedNotes, Note, NoteType, SampleExtraction
from extractor.prompt import get_extractor_prompt_template
from extractor.utils import get_messages_from_example, get_sample_as_input


def get_openai_extractor(prompt_template: ChatPromptTemplate, schema_class: BaseModel):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    return prompt_template | llm.with_structured_output(schema=schema_class)


def perform_extraction(text: str):
    extractor = get_openai_extractor(
        get_extractor_prompt_template(),
        ExtractedNotes,
    )

    examples = []
    for example in [
        SampleExtraction(
            input=get_sample_as_input("no-lessons"),
            extracted_notes=ExtractedNotes(
                notes=[
                    Note(
                        text="Price behavior during a mania",
                        type=NoteType.KEY_THEME,
                    ),
                    Note(
                        text="Corruption and its revelation during economic cycles",
                        type=NoteType.KEY_THEME,
                    ),
                    Note(
                        text="Monitor for signs of continual price increases as an indicator of a potential mania.",
                        type=NoteType.ACTION_ITEM,
                    ),
                ]
            ),
        ),
        SampleExtraction(
            input=get_sample_as_input("no-key-themes"),
            extracted_notes=ExtractedNotes(
                notes=[
                    Note(
                        text="Focusing on high-priced products can lead to significant referral commissions.",
                        type=NoteType.LESSON,
                    ),
                    Note(
                        text="Consistently posting on a blog or social media can build a steady following and generate referrals.",
                        type=NoteType.LESSON,
                    ),
                    Note(
                        text="Identify and promote high-priced products in your affiliate marketing efforts.",
                        type=NoteType.ACTION_ITEM,
                    ),
                    Note(
                        text="Develop and maintain a consistent posting schedule for your blog or social media accounts to build and sustain a follower base.",
                        type=NoteType.ACTION_ITEM,
                    ),
                ]
            ),
        ),
        SampleExtraction(
            input=get_sample_as_input("no-action-items"),
            extracted_notes=ExtractedNotes(
                notes=[
                    Note(
                        text="Opinions outside one's expertise",
                        type=NoteType.KEY_THEME,
                    ),
                    Note(
                        text="Technology and innovation to harness environmental power",
                        type=NoteType.KEY_THEME,
                    ),
                    Note(
                        text="Forceful displacement of people for development",
                        type=NoteType.KEY_THEME,
                    ),
                    Note(
                        text="Self-developed talent without formal education can lead to misguided or harmful views.",
                        type=NoteType.LESSON,
                    ),
                    Note(
                        text="Popularity can tempt individuals to opine on topics outside their expertise.",
                        type=NoteType.LESSON,
                    ),
                    Note(
                        text="Technological innovations, such as dams, can have significant environmental impacts.",
                        type=NoteType.LESSON,
                    ),
                    Note(
                        text="Development projects often involve the displacement of people, echoing past and present experiences.",
                        type=NoteType.LESSON,
                    ),
                ]
            ),
        ),
    ]:
        examples.extend(get_messages_from_example(example))

    return extractor.invoke(
        {
            "text": text,
            "examples": examples,
        }
    )
