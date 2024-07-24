from typing import Optional, TypedDict
from enum import IntEnum
from langchain_core.pydantic_v1 import BaseModel, Field


class NoteType(IntEnum):
    """The type of note. Currently only supports 1, 2, and 3."""

    KEY_THEME = 1
    LESSON = 2
    ACTION_ITEM = 3


class Note(BaseModel):
    """A description and/or summary of an idea/concept."""

    text: Optional[str] = Field(
        default=None,
        description="Text that describes and/or summarizes the idea/concept.",
    )
    type: Optional[NoteType] = Field(
        default=None,
        description="The type of note. Currently only supports 1, 2, and 3 as defined in the NoteType enum. 1 is a key theme, 2 is a lesson, and 3 is a potential action item.",
    )


class ExtractedNotes(BaseModel):
    """A collection of `Note` objects."""

    notes: list[Note]


class SampleExtraction(TypedDict):
    # the text on which extraction should be performed
    input: str

    # the notes that should be extracted
    extracted_notes: ExtractedNotes
