from typing import Protocol, List
from pydantic import BaseModel

class ResModel(BaseModel):
    score: int = 0
    error: str = ''
    reason: str = ''

class BaseLLM(Protocol):
    @classmethod
    def call_api(cls, input_data: str) -> ResModel:
        ...