import os
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from openai import OpenAI

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


class PerplexityToolInput(BaseModel):
    argument: str = Field(..., description="prompt for the perplexity API")


class PerplexityTool(BaseTool):
    name: str = "Preplexity API Tool"
    description: str = "This tool is used with the perplexity API."
    args_schema: Type[BaseModel] = PerplexityToolInput

    def _run(self, argument: str) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant and you need to "
                    "engage in a helpful, detailed, polite conversation with a user."
                ),
            },
            {
                "role": "user",
                "content": (argument),
            },
        ]
        _client = OpenAI(
            api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai"
        )

        _response = _client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
        )
        return _response.choices[0].message.content
