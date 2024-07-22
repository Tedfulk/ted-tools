from typing import List


from pydantic import BaseModel, Field


class ImageClassification(BaseModel):
    keywords: List[str] = Field(..., description="Keywords of the image.")

    def keywords_to_string(self) -> str:
        cleaned_keywords = [
            keyword.replace(" ", "_")
            for keyword in self.keywords
            if not any(char.isdigit() for char in keyword)
        ]
        joined_keywords = "_".join(cleaned_keywords)
        if joined_keywords.count("_") <= 4:
            return joined_keywords
        limited_keywords = "_".join(joined_keywords.split("_")[:4])
        return limited_keywords


# class ImageClassification(BaseModel):
#     title: str = Field(..., description="Title of the image.")
#     category: str = Field(..., description="Category of the image.")
#     style: str = Field(..., description="Style of the image.")
#     description: str = Field(
#         ..., description="Short 1 sentence description of the image."
#     )
