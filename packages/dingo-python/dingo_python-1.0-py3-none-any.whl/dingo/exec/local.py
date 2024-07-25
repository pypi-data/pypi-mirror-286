from typing import Callable, List
import os
import time
import json
import pprint

from dingo.exec.base import Executor
from dingo.convert import converters
from dingo.config import GlobalConfig
from dingo.model import Model
from dingo.model.llm.base import BaseLLM, ResModel as LLMResModel
from dingo.model.rule.base import BaseRule, ResModel as RuleResModel
from dingo.io import RawInputModel, InputModel, SummaryModel
from dingo.utils import log

QUALITY_MAP = Model.rule_metric_type_map


@Executor.register('local')
class LocalExecutor(Executor):

    def __init__(self, raw_input: RawInputModel):
        self.raw_input = raw_input

    def load_data(self, path) -> List[InputModel]:
        """
        Reads data from given path.

        Returns:
            List[InputModel]
        """
        new_raw_input = self.raw_input
        new_raw_input.input_path = path
        converter = converters[self.raw_input.data_type]
        return converter.load_data(raw_input=new_raw_input)

    def execute(self) -> List[SummaryModel]:
        """
        Executes given input models.

        Returns:

        """
        pass

    def summarize(self, input_models: List[InputModel]) -> SummaryModel:
        pass

    def walk_path(self, path_list, record, model, model_type):
        """
        Walk the path list to get
        Args:

            path_list (_type_): _description_
            record (_type_): _description_
            model (_type_): _description_
            model_type (str):
        """
        for path in path_list:
            log.debug('[Handling]:' + path)

            if os.path.isdir(path):
                for path_child in os.listdir(path):
                    path_child = path + '/' + path_child
                    path_list.append(path_child)
                continue

            if not os.path.isfile(path):
                continue
            dataset = self.load_data(path)
            if len(dataset) == 0:
                continue
            record['total'] += len(dataset)

            log.debug('[Dataset]: ' + str(dataset))
            for data in dataset:
                executor(model_type)(record, model, data)
            log.debug('[Record]: ' + str(record))
            calculate_ratio(record, model_type)
            log.debug('[Record]: ' + str(record))

    def evaluate(self) -> List[SummaryModel]:
        current_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        input_path = self.raw_input.input_path
        output_path = self.raw_input.output_path + current_time
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        record_list = []
        custom = False
        log.debug(str(self.raw_input.eval_models))
        for model_name in self.raw_input.eval_models:
            log.debug(f"[GlobalConfig.config]: {GlobalConfig.config}")
            if model_name in Model.llm_models:
                log.debug(f"[Load llm model {model_name}]")
                model = Model.llm_models[model_name]
                model_type = 'llm'
            elif model_name in Model.rule_groups:
                log.debug(f"[Load rule model {model_name}]")
                model: List[BaseRule] = Model.rule_groups[model_name]
                model_type = 'rule'
            elif GlobalConfig.config and GlobalConfig.config.custom_rule_list:
                log.debug("[Load custom rule]")
                custom = True
                model: List[BaseRule] = []
                for rule in GlobalConfig.config.custom_rule_list:
                    assert isinstance(rule, str)
                    if rule not in Model.rule_name_map:
                        raise KeyError(f"{rule} not in Model.rule_name_map, there are {str(Model.rule_name_map.keys())}")
                    model.append(Model.rule_name_map[rule])

                model_type = 'rule'
            else:
                raise KeyError('no such model: ' + model_name)
            log.debug("[ModelType]: " + model_type)
            model_path = output_path + '/' + model_name
            if not os.path.exists(model_path):
                os.makedirs(model_path)

            record = {
                'dataset_id': self.raw_input.dataset_id,
                'input_model': model_name,
                'input_path': input_path,
                'output_path': output_path,
                'score': 0,
                'num_good': 0,
                'num_bad': 0,
                'total': 0,
                'error_info': {},
            }
            path_list = [input_path]
            self.walk_path(path_list, record, model, model_type)

            # pprint.pprint(record, sort_dicts=False)
            if model_type == 'rule':
                summary = write_data_rule(record, model_path)
            elif model_type == 'llm':
                summary = write_data_llm(record, model_path)
            else:
                raise KeyError('no such model: ' + model_type)

            record_list.append(summary)
            if custom:
                break
        log.debug(record_list)
        return record_list


def get_quality_signal(rule: Callable):
    for quality_signal in QUALITY_MAP:
        for rule_class in QUALITY_MAP[quality_signal]:
            if rule.__name__ == rule_class.__name__:
                return quality_signal

    raise RuntimeError('this rule can not find its quality_signal: ' + rule.__name__)


def write_data_rule(record, path):
    summary = SummaryModel(
        dataset_id = record['dataset_id'],
        input_model = record['input_model'],
        input_path = record['input_path'],
        output_path = record['output_path'],
        score = record['score'],
        num_good = record['num_good'],
        num_bad = record['num_bad'],
        total = record['total'],
        error_ratio = {}
    )

    for quality_signal in record['error_info']:
        summary.error_ratio[quality_signal] = 0
        if record['error_info'][quality_signal]['count'] == 0:
            continue

        if not os.path.exists(path + "/{}".format(quality_signal)):
            os.makedirs(path + "/{}".format(quality_signal))
        summary.error_ratio[quality_signal] = round(record['error_info'][quality_signal]['count'] / record['total'], 6)
        for rule_name in record['error_info'][quality_signal]:
            if rule_name in ['count',]:
                continue
            with open(path + '/{}/{}.json'.format(quality_signal, rule_name), 'w', encoding='utf-8') as f:
                json.dump(record['error_info'][quality_signal][rule_name], f, indent=4, ensure_ascii=False)

    with open(path + '/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary.to_dict(), f, indent=4, ensure_ascii=False)
    return summary


def write_data_llm(record, path):
    summary = SummaryModel(
        dataset_id=record['dataset_id'],
        input_model=record['input_model'],
        input_path=record['input_path'],
        output_path=record['output_path'],
        score=record['score'],
        num_good=record['num_good'],
        num_bad=record['num_bad'],
        total=record['total'],
        error_ratio={},
    )

    for error_type in record['error_info']:
        summary.error_ratio[error_type] = record['error_info'][error_type]['ratio']
        with open(path + '/{}.json'.format(error_type), 'w', encoding='utf-8') as f:
            json.dump(record['error_info'][error_type], f, indent=4, ensure_ascii=False)

    with open(path + '/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary.to_dict(), f, indent=4, ensure_ascii=False)
    return summary


def execute_rule(record, rule_map, d: InputModel):
    if_good = True
    if_qs_good = {}
    for q_s in QUALITY_MAP:
        if_qs_good[q_s] = True
        if q_s not in record['error_info']:
            record['error_info'][q_s] = {'count': 0}
    log.debug("[RuleMap]: " + str(rule_map))
    for r in rule_map:
        r_n = r.__name__
        # execute rule
        if r_n.startswith('Prompt'):
            tmp: RuleResModel = r.eval([d.prompt, d.content])
        else:
            tmp: RuleResModel = r.eval([d.content])
        # analyze result
        if not tmp.error_status:
            continue
        if_good = False
        q_s = get_quality_signal(r)
        if_qs_good[q_s] = False
        if r_n not in record['error_info'][q_s]:
            record['error_info'][q_s][r_n] = {'name': r_n, 'count': 0, 'ratio': 0, 'detail': []}
        record['error_info'][q_s][r_n]['count'] += 1
        record['error_info'][q_s][r_n]['detail'].append(
            {'data_id': d.data_id, 'prompt': d.prompt, 'content': d.content, 'error_reason': tmp.error_reason})

    if not if_good:
        record['num_bad'] += 1
        for q_s in if_qs_good:
            if not if_qs_good[q_s]:
                record['error_info'][q_s]['count'] += 1


def execute_llm(record, llm: BaseLLM, d: InputModel):
    tmp: LLMResModel = llm.call_api(d.content)
    if tmp.score > 6:
        return

    record['num_bad'] += 1
    e = tmp.error
    if e not in record['error_info']:
        record['error_info'][e] = {'name': e, 'count': 0, 'ratio': 0, 'detail': []}
    record['error_info'][e]['count'] += 1
    record['error_info'][e]['detail'].append(
        {'api_score': tmp.score, 'data_id': d.data_id, 'prompt': d.prompt, 'content': d.content,
         'error_reason': tmp.reason})


def calculate_ratio(record, model_type):
    record['num_good'] = record['total'] - record['num_bad']
    record['score'] = round(record['num_good'] / record['total'] * 100, 2)
    if model_type == 'rule':
        for q_s in record['error_info']:
            for r_n in record['error_info'][q_s]:
                if r_n in ['count',]:
                    continue
                record['error_info'][q_s][r_n]['ratio'] = round(record['error_info'][q_s][r_n]['count'] / record['total'], 6)
    else:
        for e in record['error_info']:
            record['error_info'][e]['ratio'] = round(record['error_info'][e]['count'] / record['total'], 6)


def executor(model_type: str) -> Callable:
    if model_type == 'rule':
        return execute_rule
    if model_type == 'llm':
        return execute_llm
    raise RuntimeError(f'Unsupported model type: {model_type}')


def write_data(model_type: str) -> Callable:
    if model_type == 'rule':
        return write_data_rule
    if model_type == 'llm':
        return write_data_llm
