import enum
from pydantic import BaseModel


class ContentType(str, enum.Enum):
    """Enumeration for single text classification."""

    BRIEF = "brief"
    DETAILED = "detailed"


class SinglePrediction(BaseModel):
    """Class for a single class label prediction."""

    class_label: ContentType
