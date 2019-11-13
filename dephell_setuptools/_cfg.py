from copy import deepcopy
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, List, Optional, Union

from setuptools.config import ConfigOptionsHandler, ConfigMetadataHandler

from ._base import BaseReader
from ._constants import FIELDS


class CfgReader(BaseReader):
    def __init__(self, path: Union[str, Path]):
        self.path = self._normalize_path(path, default_name='setup.cfg')

    @property
    def content(self) -> Optional[Dict[str, Union[List, Dict]]]:
        path = self.path
        if path.name == 'setup.py':
            path = path.parent / 'setup.cfg'
            if not path.exists():
                raise FileNotFoundError(str(path))

        parser = ConfigParser()
        parser.read(str(path))

        options = deepcopy(parser._sections)
        for section, content in options.items():
            for k, v in content.items():
                options[section][k] = ('', v)

        container = type('container', (), dict.fromkeys(FIELDS))()
        ConfigOptionsHandler(container, options).parse()
        ConfigMetadataHandler(container, options).parse()

        return self._clean(vars(container))
