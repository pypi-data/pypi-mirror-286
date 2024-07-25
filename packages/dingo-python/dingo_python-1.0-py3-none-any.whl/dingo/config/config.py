from typing import Optional, List, Dict
import json

from pydantic import BaseModel

from dingo.utils import log


class DynamicRuleConfig(BaseModel):
    threshold: Optional[float] = None
    pattern: Optional[str] = None
    key_list: Optional[List[str]] = None
    file_path: Optional[str] = None

class DynamicLLMConfig(BaseModel):
    path: Optional[str] = None
    key: Optional[str] = None
    api_url: Optional[str] = None

class Config(BaseModel):
    custom_rule_list: Optional[List[str]] = []
    rule_config: Optional[Dict[str, DynamicRuleConfig]] = {}
    llm_config: Optional[Dict[str, DynamicLLMConfig]] = {}


class GlobalConfig:
    config = None

    @classmethod
    def read_config_file(cls, custom_config_path: Optional[str]):
        if custom_config_path is None:
            cls.config = Config()
            return
        try:
            with open(custom_config_path, "r") as f:
                rule_json = json.load(f)
        except FileNotFoundError:
            log.error("No config file found, error path.")

        try:
            cls.config = Config(
                custom_rule_list=rule_json.get('custom_rule_list', []),
                rule_config={i: DynamicRuleConfig(**rule_config) for i, rule_config in rule_json.get('rule_config', {}).items()},
                llm_config={i: DynamicLLMConfig(**llm_config) for i, llm_config in rule_json.get('llm_config', {}).items()},
            )
        except Exception as e:
            raise RuntimeError(f"Error loading config: {e}")
