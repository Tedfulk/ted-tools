import re
from typing import List

from pydantic import BaseModel, Field, field_validator


class Titles(BaseModel):
    titles: List[str] = Field(
        ...,
        description="List of 3 titles about the video",
        min_items=1,
        max_items=3,
        examples=[
            "Mojo Is FASTER Than Rust By 50%",
            "I Spent 50 Hours Buried Alive",
            "2.1 Billion Downloaded Deprecated Packages NPM",
        ],
    )


class Description(BaseModel):
    title: str = Field(
        ...,
        description="Title of the description.",
    )
    description: str = Field(
        ...,
        description="An SEO driven description for the video that will be used on YouTube. This should be 50 words.",
    )


class Transcript(BaseModel):
    title: str = Field(
        ...,
        description="Title of the transcript.",
    )
    transcript: str = Field(
        ...,
        description="The transcript for the video that will have a introduction, supporting sections of conversation, and a conclusion.",
    )


class Script(BaseModel):
    title: str = Field(
        ...,
        description="Title of the script.",
    )
    script: str = Field(
        ...,
        description="The script for the video that will have a introduction, supporting sections of conversation, and a conclusion.",
    )

    @field_validator("title")
    def validate_title(cls, value: str):
        # remove all non-alphanumeric characters
        value = re.sub(r"[^a-zA-Z0-9]", "", value)
        # replace all white space with "-"
        value = value.replace(" ", "-")
        return value


class ThumbnailPrompts(BaseModel):
    thumbnail_prompts: List[str] = Field(
        ...,
        description="List of 3 prompts for the thumbnail for this video",
        min_items=1,
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
        description="List of 10 hashtags for this video",
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
            if not v.startswith("#"):
                v = f"#{v}"
            elif " " in v:
                v = v.replace(" ", "")
            elif not v.isalnum():
                v = re.sub(r"[^a-zA-Z0-9]", "", v[1:])
            else:
                raise ValueError(
                    "each hashtag must start with #, contain no spaces, and must be alphanumeric"
                )
        return values


class YoutubeMetadata(BaseModel):
    titles: List[str] = Field(
        ...,
        description="List of 3 titles about the video",
        min_items=1,
        max_items=3,
        examples=[
            "Mojo Is FASTER Than Rust By 50%",
            "I Spent 50 Hours Buried Alive",
            "2.1 Billion Downloaded Deprecated Packages NPM",
        ],
    )
    description: str = Field(
        ...,
        description="An SEO driven description for the video that will be used on YouTube. This should be 50 words.",
    )
    transcript: str = Field(
        ...,
        description="The transcript for the video that will have a introduction, supporting sections of conversation, and a conclusion.",
    )
    thumbnail_prompts: List[str] = Field(
        ...,
        description="List of 3 prompts for the thumbnail for this video",
        min_items=1,
        max_items=3,
        examples=[
            "Illustrate 'Mojo' leading 'Rust' in a futuristic race, with speed lines and digital motifs.",
            "Show a clock at 50 hours over a dim, underground space, hinting at light from above.",
            "Depict a digital landfill of old NPM packages with '2.1 Billion' visible, and a modern deprecated packages warning.",
        ],
    )
    hashtags: List[str] = Field(
        ...,
        description="List of 10 hashtags for this video",
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
