from typing import List, Dict

from pydantic import BaseModel


class SummaryModel(BaseModel):
    dataset_id: str
    input_model: str
    input_path: str
    output_path: str
    score: float
    num_good: int
    num_bad: int
    total: int
    error_ratio: Dict[str, float]

    def to_dict(self):
        return {
            'dataset_id': self.dataset_id,
            'input_model': self.input_model,
            'input_path': self.input_path,
            'output_path': self.output_path,
            'score': self.score,
            'num_good': self.num_good,
            'num_bad': self.num_bad,
            'total': self.total,
            'error_ratio': self.error_ratio
        }
