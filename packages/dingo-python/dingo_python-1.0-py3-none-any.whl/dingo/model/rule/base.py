from typing import Protocol, List, Union
from pydantic import BaseModel


class ResModel(BaseModel):
    error_status: bool = False
    error_reason: str = ''


class BaseRule(Protocol):

    @classmethod
    def eval(cls, input_data: List[str]) -> ResModel:
        ...
