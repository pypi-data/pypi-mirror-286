import uuid
import json
import orjson

from abc import ABC, abstractmethod
from typing import Protocol, List, Dict, Any, Callable, Optional

from pyspark import SparkConf
from pyspark.sql import SparkSession, Row, DataFrame
from pyspark.sql.functions import explode, count, col, format_number
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, ArrayType

from dingo.model import Model
from dingo.model.rule.base import BaseRule, ResModel as RuleResModel

QUALITY_MAP = Model.rule_metric_type_map

class SparkExecutor():
    def __init__(self):
        self.spark: Optional[SparkSession] = None
        self.input_df: Optional[DataFrame] = None
        self.convert_df: Optional[DataFrame] = None
        self.output_df: Optional[DataFrame] = None
        self.summary = {
            'score': 0.0,
            'num_good': 0,
            'num_bad': 0,
            'total': 0,
            'error_ratio': {
                "QUALITY_SIGNAL_EFFECTIVENESS": 0.0,
                "QUALITY_SIGNAL_COMPLETENESS": 0.0,
                "QUALITY_SIGNAL_UNDERSTANDABILITY": 0.0,
                "QUALITY_SIGNAL_SIMILARITY": 0.0,
                "QUALITY_SIGNAL_FLUENCY": 0.0,
                "QUALITY_SIGNAL_RELEVANCE": 0.0,
                "QUALITY_SIGNAL_SECURITY": 0.0
            }
        }

    def set_spark(self, spark: SparkSession):
        self.spark = spark

    def set_input_df(self, df: DataFrame):
        self.input_df = df

    def get_spark(self):
        return self.spark

    def get_input_df(self):
        return self.input_df

    def get_convert_df(self):
        return self.convert_df

    def get_output_df(self):
        return self.output_df

    def get_summary(self):
        return self.summary

    def create_spark(self, conf: SparkConf):
        try:
            self.spark = SparkSession.builder.config(conf=conf).enableHiveSupport().getOrCreate()  # type: ignore
        except:
            self.spark = SparkSession.builder.config(conf=conf).getOrCreate()  # type: ignore

    def convert_data(
            self,
            column_content: List[str],
            column_id: List[str] = None,
            column_prompt: List[str] = None,
    ):
        def func(row: Row) -> Row:
            data = orjson.loads(row.value)
            new_data = {
                'data_id': find_nested_data(data, column_id) if column_id is not None else str(uuid.uuid4()),
                'prompt': find_nested_data(data, column_prompt) if column_prompt is not None else '',
                'content': find_nested_data(data, column_content),
            }
            return Row(value=orjson.dumps(new_data).decode("utf-8"))

        convert_df = self.input_df.rdd.map(func).toDF()
        self.summary['total'] = convert_df.count()
        self.convert_df = convert_df

    # # @abstractmethod
    # # def evaluate(self) -> List[SummaryModel]:
    # #     raise NotImplementedError()

    def summarize(self):
        self.summary['num_good'] = self.summary['total'] - self.summary['num_bad']
        self.summary['score'] = round(self.summary['num_good'] / self.summary['total'] * 100, 2) if self.summary['total'] != 0 else 0

        def extract_error_info(row):
            data = orjson.loads(row.value)
            return Row(id=data['data_id'], error_functions=data['quality_signals'])

        schema = StructType([
            StructField("data_id", StringType(), True),
            StructField("quality_signals", ArrayType(StringType()), True)
        ])

        df_error_info = self.spark.createDataFrame(self.output_df.rdd.map(extract_error_info), schema=schema)

        df_exploded = df_error_info.select("data_id", explode("quality_signals").alias("quality_signal"))
        df_grouped = df_exploded.groupBy("quality_signal").agg(count("*").alias("count"))
        df_grouped = df_grouped.withColumn("ratio", format_number(col("count") / self.summary["total"], 6))

        rows = df_grouped.collect()
        for row in rows:
            quality_signal = row['quality_signal']
            ratio = row['ratio']
            self.summary['error_ratio'][quality_signal] = ratio

    def execute(self, rule_list: List[str]):
        def func_exec(row: Row):
            data = orjson.loads(row.value)
            new_data = execute_rule(rule_list, data)
            return Row(value=orjson.dumps(new_data).decode("utf-8"))

        def func_filter(row: Row):
            return orjson.loads(row.value)['error_status'] is True

        self.output_df = self.convert_df.rdd.map(func_exec).toDF()
        self.output_df = self.output_df.rdd.filter(func_filter).toDF()
        self.summary['num_bad'] = self.output_df.count()


def find_nested_data(jsn: json, levels: List[str]):
    data = jsn
    for key in levels:
        data = data[key]
    return data

def get_quality_signal(rule: BaseRule):
    for quality_signal in QUALITY_MAP:
        for rule_class in QUALITY_MAP[quality_signal]:
            if rule.__name__ == rule_class.__name__:
                return quality_signal

    raise RuntimeError('this rule can not find its quality_signal: ' + rule.__name__)

def execute_rule(rule_list: List[str], data: json) -> json:
    data['error_status'] = False
    data['error_functions'] = []
    data['quality_signals'] = []

    model: List[BaseRule] = []
    for rule in rule_list:
        assert isinstance(rule, str)
        if rule not in Model.rule_name_map:
            raise KeyError(f"{rule} not in Model.rule_name_map, there are {str(Model.rule_name_map.keys())}")
        model.append(Model.rule_name_map[rule])

    for rule_class in model:
        rule_name = rule_class.__name__
        if rule_name.startswith('Prompt'):
            tmp: RuleResModel = rule_class.eval([data["prompt"], data["content"]])
        else:
            tmp: RuleResModel = rule_class.eval([data["content"]])

        if tmp.error_status:
            data['error_status'] = True
            data['error_functions'].append(rule_name)
            quality_signal = get_quality_signal(rule_class)
            if quality_signal not in data['quality_signals']:
                data['quality_signals'].append(quality_signal)

    return data
