import logging
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

TOP_DIR = Path(__file__).resolve().parent.parent
LOGGER = logging.getLogger(__name__)
DEFAULT_CONFIG = {
    'Client ID': None,
    'Access Token': None,
    'Refresh Token': None
}


def setup_yaml() -> YAML:
    def null_representer(self, data):
        return self.represent_scalar(u'tag:yaml.org,2002:null', u'~')

    yaml = YAML(pure=True)
    yaml.default_flow_style = False
    yaml.width = 2147483647
    yaml.representer.add_representer(type(None), null_representer)
    # yaml.emitter.alt_null = '~'
    yaml.version = (1, 2)
    return yaml


def save_config(data: CommentedMap, testing: bool = False):
    config_file = TOP_DIR.joinpath('config-test.yaml' if testing else 'config.yaml')
    with open(config_file, 'w', encoding='UTF-8') as yaml_file:
        setup_yaml().dump(data, yaml_file)


def load_config(testing: bool = False) -> CommentedMap:
    def validate_config(config: CommentedMap) -> CommentedMap:
        for key, value in DEFAULT_CONFIG.copy().items():
            if key not in config:
                config[key] = value
            if isinstance(value, dict):
                for sub_key, sub_value in value.copy().items():
                    if sub_key not in config[key]:
                        config[key][sub_key] = sub_value
        return config

    config_file = TOP_DIR.joinpath('config-test.yaml' if testing else 'config.yaml')
    if config_file.exists():
        with open(config_file, 'r', encoding='UTF-8') as yaml_file:
            data = setup_yaml().load(yaml_file) or DEFAULT_CONFIG
    else:
        config_file.touch()
        data = DEFAULT_CONFIG
    validate_config(data)
    save_config(data, testing)
    return data


CONFIG = load_config()
