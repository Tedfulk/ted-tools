import re
from typing import List

from pydantic import BaseModel, Field, field_validator


class Titles(BaseModel):
    titles: List[str] = Field(
        ...,
        description="List of 3 titles about the video",
        min_items=3,
        max_items=3,
        examples=[
            "Mojo Is FASTER Than Rust By 50%",
            "I Spent 50 Hours Buried Alive",
            "2.1 Billion Downloaded Deprecated Packages NPM",
        ],
    )


class Description(BaseModel):
    description: str = Field(
        ...,
        description="An SEO driven description for the video that will be used on YouTube. This should be 50 words.",
    )


class Transcript(BaseModel):
    transcript: str = Field(
        ...,
        description="The transcript for the video that will have a introduction, supporting sections of conversation, and a conclusion.",
    )


class ThumbnailPrompts(BaseModel):
    thumbnail_prompts: List[str] = Field(
        ...,
        description="List of 3 prompts for the thumbnail for this video",
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
        description="List of 10 hashtags for this video",
        min_items=10,
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
        min_items=3,
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
        examples="This tutorial covers the basics of the Python programming language, specifically focusing on its use with the itertools module. The itertools module provides various functions that help manipulate iterators, allowing for efficient looping and iteration over sequences or other data structures. The video will provide step-by-step explanations on how to use these functions, covering topics such as combinations, permutations, and creating infinite iterators. By the end of the video, viewers will have a solid understanding of Python's itertools module and how to utilize it in their own coding projects.",
    )
    transcript: str = Field(
        ...,
        description="The transcript for the video that will have a introduction, supporting sections of conversation, and a conclusion.",
        examples="Hello everyone, today we're going to talk about python and the itertools module. Firstly, let me give you an introduction to python. It is a high-level programming language that is easy to learn and use, making it perfect for beginners in programming. Python is also very versatile and can be used in various applications such as web development, data analysis, artificial intelligence, and more. Now let's move on to the itertools module. This module provides functions for handling iterators and working with sequences of data. It is useful when you need to perform operations on a sequence of data without having to create a new list or modify the original one. The itertools module contains various functions such as count(), cycle(), repeat(), and more, which can be used to create different types of iterators. In this video, we will explore some examples of how to use the itertools module in Python. We'll start with simple examples like creating a list of numbers using the count() function and then move on to more complex ones that involve generating permutations and combinations of elements in a sequence. So stay tuned for an informative video on python and itertools. Thank you for watching!",
    )
    thumbnail_prompts: List[str] = Field(
        ...,
        description="List of 3 prompts for the thumbnail for this video",
        min_items=3,
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
        min_items=10,
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
