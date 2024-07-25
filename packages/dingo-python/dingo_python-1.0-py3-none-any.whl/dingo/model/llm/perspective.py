import pprint

from dingo.model import Model
from dingo.model.llm.base import BaseLLM, ResModel

try:
    from googleapiclient import discovery
except ImportError:
    raise ImportError('googleapiclient not installed, please install it with `pip install google-api-python-client`')

@Model.llm_register('perspective')
class Perspective(BaseLLM):
    key = ''
    api_url = 'https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1'

    client = None

    @classmethod
    def create_client(cls):
        if cls.client is None:
            cls.client = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=cls.key,
                discoveryServiceUrl=cls.api_url,
                static_discovery=False,
            )

    @classmethod
    def call_api(cls, input_data: str) -> ResModel:
        cls.create_client()
        analyze_request = {
            'comment': {'text': input_data},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'IDENTITY_ATTACK': {},
                'INSULT': {},
                'PROFANITY': {},
                'THREAT': {},
                # 'SEXUALLY_EXPLICIT': {},
                # 'FLIRTATION': {},
            }
        }

        try:
            response = cls.client.comments().analyze(body=analyze_request).execute()
            result = ResModel()
            is_good = True
            error_list = []
            for e in response['attributeScores']:
                value = response['attributeScores'][e]['summaryScore']['value']
                if value > 0.6:
                    is_good = False
                    error_list.append(e)
            if is_good is True:
                result.score = 10
            else:
                result.score = 0
                result.error = 'ERROR_PERSPECTIVE'
                result.reason = ",".join(error_list)
            return result
        except RuntimeError:
            return ResModel(
                score=0,
                error='API_LOSS',
                reason=''
            )