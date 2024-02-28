import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from a .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

# API Endpoints
OLLAMA_API_ENDPOINT = os.getenv("OLLAMA_API_ENDPOINT", "http://127.0.0.1:11434/v1")
YOUTUBE_API_ENDPOINT = os.getenv(
    "YOUTUBE_API_ENDPOINT", "https://www.googleapis.com/youtube/v3"
)

# Default file paths
DEFAULT_METADATA_DIR = os.getenv("DEFAULT_METADATA_DIR", "ted_tools/data")

# Application settings
DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "t"]


class Config(BaseModel):
    user: str = Field(description="Username", examples="Ted", default="Ted")
    emoji: str = Field(
        description="Emoji to use for the user", examples="👉", default="👉"
    )
    model: str = Field(
        description="Model to use",
        examples="dolphin-mixtral:8x7b-v2.7-q4_K_M",
        default="dolphin-mixtral:8x7b-v2.7-q4_K_M",
    )
