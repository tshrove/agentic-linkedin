import os
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from openai import OpenAI

XAI_API_KEY = os.getenv("XAI_API_KEY")


class GrokToolInput(BaseModel):
    argument: str = Field(..., description="prompt for the grok API")


class GrokTool(BaseTool):
    name: str = "Grok API Tool"
    description: str = "This tool is used with the grok API."
    args_schema: Type[BaseModel] = GrokToolInput

    def _run(self, argument: str) -> str:
        _client = OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1",
        )

        _completion = _client.chat.completions.create(
            model="grok-2-latest",
            messages=[
                {
                    "role": "user",
                    "content": argument,
                },
            ],
        )
        _output:str = _completion.choices[0].message.content
        return _output
