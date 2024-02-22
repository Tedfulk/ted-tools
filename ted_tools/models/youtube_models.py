import re
from typing import List
from pydantic import BaseModel, Field, field_validator, ValidationError


class Titles(BaseModel):
    title: List[str] = Field(
        ...,
        title="List of 3 titles about the video",
        min_items=3,
        max_items=3,
        examples=[
            "Mojo Is FASTER Than Rust By 50%",
            "I Spent 50 Hours Buried Alive",
            "2.1 Billion Downloaded Deprecated Packages NPM",
        ],
    )


class Description(BaseModel):
    description: str


class Transcript(BaseModel):
    transcript: str


class ThumbnailPrompts(BaseModel):
    thumbnail_prompts: List[str] = Field(
        ...,
        title="List of 3 prompts for the thumbnail for this video",
        min_items=3,
        max_items=3,
        examples=[
            "Illustrate 'Mojo' leading 'Rust' in a futuristic race, with speed lines and digital motifs.",
            "Show a clock at 50 hours over a dim, underground space, hinting at light from above.",
            "Depict a digital landfill of old NPM packages with '2.1 Billion' visible, and a modern deprecated packages warning.",
        ],
    )


class Hashtags(BaseModel):
    hashtags: List[str] = Field(
        ...,
        title="List of 10 hashtags for this video",
        min_items=5,
        max_items=10,
        examples=[
            "#MojoVsRust",
            "#BuriedAliveChallenge",
            "#NPMWarnings",
            "#CodingTutorials",
            "#TechUpdates",
            "#DeveloperLife",
            "#SoftwareEngineering",
            "#ProgrammingHumor",
            "#TechCommunity",
            "#OpenSource",
        ],
    )

    @field_validator("hashtags")
    def validate_hashtag(cls, values: str):
        for v in values:
            if not re.match(r"^#[^\s]+$", v):
                raise ValueError("each hashtag must start with # and contain no spaces")
            return values


class YoutubeMetadata(BaseModel):
    titles: Titles
    description: Description
    transcript: Transcript
    thumbnail_prompts: ThumbnailPrompts
    hashtags: Hashtags
