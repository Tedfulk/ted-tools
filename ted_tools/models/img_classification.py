import enum
from typing import List

from pydantic import BaseModel, Field


class ImageClassification(BaseModel):
    title: str = Field(..., description="Title of the image.")
    category: str = Field(..., description="Category of the image.")
    style: str = Field(..., description="Style of the image.")
    description: str = Field(
        ..., description="Short 1 sentence description of the image."
    )
