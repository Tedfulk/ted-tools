import enum
from pydantic import BaseModel


class ContentType(str, enum.Enum):
    """Enumeration for a single text classification."""

    TITLE = "title"
    TUTORIAL = "tutorial"


class SinglePrediction(BaseModel):
    """Class for a single ContentType prediction."""

    content_type: ContentType


# TODO: Think about an SPR and SPRDecopressor enum and an encompassing LLMSummary class.
