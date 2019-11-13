from pathlib import Path
from typing import Union

from ._constants import FIELDS


class BaseReader:
    def __init__(self, path: Union[str, Path]):
        self.path = self._normalize_path(path, default_name='setup.py')

    @staticmethod
    def _normalize_path(path: Union[str, Path], default_name: str) -> Path:
        if isinstance(path, str):
            path = Path(path)
        if not path.exists():
            raise FileNotFoundError(str(path))
        if path.is_dir():
            path /= default_name
        return path

    @staticmethod
    def _clean(data: dict):
        result = dict()
        for k, v in data.items():
            if k not in FIELDS:
                continue
            if not v or v == 'UNKNOWN':
                continue
            result[k] = v

        # split keywords string by words
        if 'keywords' in result:
            if isinstance(result['keywords'], str):
                result['keywords'] = [result['keywords']]
            result['keywords'] = sum((kw.split() for kw in result['keywords']), [])

        return result
