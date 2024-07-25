from functools import wraps
from typing import List, Protocol
import json

from dingo.io import InputModel, RawInputModel
from dingo.utils import log


class ConverterProto(Protocol):
    @classmethod
    def load_data(cls, raw_input: RawInputModel) -> List[InputModel]:
        ...


class BaseConverter(ConverterProto):
    converters = {}

    def __init__(self):
        pass

    @classmethod
    def load_data(cls, raw_input: RawInputModel) -> List[InputModel]:
        raise NotImplementedError()

    @classmethod
    def register(cls, type_name: str):
        def decorator(root_class):
            cls.converters[type_name] = root_class

            @wraps(root_class)
            def wrapped_function(*args, **kwargs):
                return root_class(*args, **kwargs)

            return wrapped_function

        return decorator

    @classmethod
    def find_levels_data(cls, data: json, levels: List[str]):
        res = data
        for key in levels:
            res = res[key]
        return res


@BaseConverter.register('json')
class JsonConverter(BaseConverter):
    """
    Json file converter.
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def load_data(cls, raw_input: RawInputModel) -> List[InputModel]:
        log.debug("Loading data from json file")
        raw_data = []
        with open(raw_input.input_path, 'r', encoding='utf-8') as f:
            s = f.read()
            j = json.loads(s)
            for k, v in j.items():
                raw_data.append(InputModel(**{
                    'data_id': cls.find_levels_data(v, raw_input.column_id) if raw_input.column_id != [] else str(k),
                    'prompt': cls.find_levels_data(v, raw_input.column_prompt) if raw_input.column_prompt != [] else '',
                    'content': cls.find_levels_data(v, raw_input.column_content)

                }))
        return raw_data


@BaseConverter.register('plaintext')
class PlainConverter(BaseConverter):
    """
    Plain text file converter
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def load_data(cls, raw_input: RawInputModel) -> List[InputModel]:
        log.debug("Loading data from plaintext file")
        data_id = 0
        raw_data = []
        with open(raw_input.input_path, 'r', encoding='utf-8') as f:
            for line in f:
                raw_data.append(InputModel(**{
                    'data_id': str(data_id),
                    'prompt': '',
                    'content': line
                }))
                data_id += 1
        return raw_data


@BaseConverter.register('jsonl')
class JsonLineConverter(BaseConverter):
    """
    Json line file converter.
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def load_data(cls, raw_input: RawInputModel) -> List[InputModel]:
        log.debug("Loading data from jsonl file")
        data_id = 0
        raw_data = []
        with open(raw_input.input_path, 'r', encoding='utf-8') as f:
            for j_l in f:
                j = json.loads(j_l)
                raw_data.append(InputModel(**{
                    'data_id': cls.find_levels_data(j, raw_input.column_id) if raw_input.column_id != [] else str(data_id),
                    'prompt': cls.find_levels_data(j, raw_input.column_prompt) if raw_input.column_prompt != [] else '',
                    'content': cls.find_levels_data(j, raw_input.column_content)
                }))
                data_id += 1
        return raw_data

@BaseConverter.register('listjson')
class ListJsonConverter(BaseConverter):
    """
    List json file converter.
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def load_data(cls, raw_input: RawInputModel) -> List[InputModel]:
        log.debug("Loading data from list json file")
        data_id = 0
        raw_data = []
        with open(raw_input.input_path, 'r', encoding='utf-8') as f:
            s = f.read()
            l_j = json.loads(s)
            for j in l_j:
                raw_data.append(InputModel(**{
                    'data_id': cls.find_levels_data(j, raw_input.column_id) if raw_input.column_id != [] else str(data_id),
                    'prompt': cls.find_levels_data(j, raw_input.column_prompt) if raw_input.column_prompt != [] else '',
                    'content': cls.find_levels_data(j, raw_input.column_content)

                }))
                data_id += 1
        return raw_data