import json
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM

from dingo.model import Model
from dingo.model.llm.base import BaseLLM, ResModel

try:
    import torch
except ImportError as e:
    raise ImportError("You need to install `torch`, try `pip install torch`")

@Model.llm_register('llama3')
class LLaMa3(BaseLLM):
    path = ''

    model = None
    tokenizer = None
    general_filter = """
            Please rate the following sentences based on their fluency, completeness, and level of repetition. 
            The scores from low to high indicate the quality of the sentences, with values ranging from 0 to 10 and reasons given. 
            Please provide a JSON format reply containing the specified key and value.
            requirement:
            -The returned content must be in JSON format and there should be no extra content.
            -The first key returned is score, which is an integer between 0 and 10.
            -The second key returned is error, with a value of one of the following: unsmooth, incomplete, or repetitive. If the sentence is correct, this value is empty.
            -The third key returned is reason, and the value is the reason for scoring.
            -If the sentence is empty, please give it a score of 0.


            %s

            """

    @classmethod
    def generate_words(cls, input_data: str) -> json:
        if cls.model is None:
            cls.model = AutoModelForCausalLM.from_pretrained(
                cls.path,
                torch_dtype=torch.bfloat16,
                device_map="auto",
            )
        if cls.tokenizer is None:
            cls.tokenizer = AutoTokenizer.from_pretrained(cls.path)

        messages = [
            {"role": "system", "content": input_data},
        ]

        input_ids = cls.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(cls.model.device)

        terminators = [
            cls.tokenizer.eos_token_id,
            cls.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = cls.model.generate(
            input_ids,
            max_new_tokens=256,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        response = outputs[0][input_ids.shape[-1]:]
        return json.loads(cls.tokenizer.decode(response, skip_special_tokens=True))

    @classmethod
    def check_key(cls, data: json):
        key_list = ['score', 'error', 'reason']
        for key in key_list:
            if key not in data:
                return False
        return True

    @classmethod
    def call_api(cls, input_data: str) -> ResModel:
        try:
            response = cls.generate_words(cls.general_filter % input_data)
            if cls.check_key(response) is False:
                raise RuntimeError('miss key: score, error, reason')

            return ResModel(
                score=response['score'],
                error=response['error'],
                reason=response['reason']
            )
        except RuntimeError:
            return ResModel(
                score=0,
                error='API_LOSS',
                reason=''
            )