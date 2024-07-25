import time
from typing import Optional, List
from pydantic import BaseModel


class InputModel(BaseModel):
    """
    Input model, output of converter.
    """
    data_id: str
    prompt: str
    content: str


class RawInputModel(BaseModel):
    """
    Dataset model, output of converter.
    """
    dataset_id: str = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    eval_models: List[str] = ['default']
    input_path: str = "data/inputs/test_data1.json"
    output_path: str = "data/outputs/"
    data_type: str = "json"
    column_content: List[str] = []
    column_id: List[str] = []
    column_prompt: List[str] = []
    custom_config_path: Optional[str] = None