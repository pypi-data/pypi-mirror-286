import yaml
import logging
from typing import Literal
from ..errors import YamlParseError


class Settings(dict):
    """
    Represents app settings yaml file
    """

    def __init__(self, section: Literal['llm', 'embeddings', 'vectordb'], path='./app-settings.yaml', **kwargs):
        """
        Reads given yaml file
        - Use kwargs to override values
        """
        self.path = path
        self.section = section

        try:
            # read yaml file
            yaml_content = self._read_yaml(path)

            # add values
            yaml_section = yaml_content[section]
            for key, value in yaml_section.items():
                self[key] = value

            # override values
            self.update({
                key: value
                for key, value in kwargs.items()
            })

        except Exception as ex:
            logging.error(
                f"Failed to read '{section}' section from '{self.path}'. Original: {ex}")
            raise

    def _read_yaml(self, path):
        try:
            with open(path, 'r') as file:
                yaml_content = yaml.safe_load(file)
                return yaml_content
        except FileNotFoundError:
            raise
        except Exception as ex:
            raise YamlParseError(
                f"File '{self.path}' could not be parsed correcty to yaml! Original: {ex}")
