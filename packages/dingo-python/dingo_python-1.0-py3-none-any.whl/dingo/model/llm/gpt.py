import json

from dingo.model import Model
from dingo.model.llm.common.openai_api import OpenAI
from dingo.model.llm.base import BaseLLM, ResModel
from dingo.utils import log

@Model.llm_register('gpt')
class GPT(BaseLLM):
    key = ''

    gpt_client = None
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
    def create_client(cls):
        if cls.gpt_client is None:
            cls.gpt_client = OpenAI('gpt-4', key=cls.key)

    @classmethod
    def check_key(cls, data: json):
        key_list = ['score', 'error', 'reason']
        for key in key_list:
            if key not in data:
                return False
        return True

    @classmethod
    def call_api(cls, input_data: str) -> ResModel:
        cls.create_client()
        response = cls.gpt_client.generate([cls.general_filter % input_data])
        log.debug(response)
        try:
            response = json.loads(response[0])
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
