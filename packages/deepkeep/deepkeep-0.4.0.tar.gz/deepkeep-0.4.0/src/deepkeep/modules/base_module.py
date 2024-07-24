from dataclasses import dataclass, fields, asdict
from typing import Union

import requests
from deepkeep._exceptions import DeepkeepError


class BaseModule:
    root_path: str = "/"
    _client: 'DeepKeep'
    _DEFAULT_HOST_ = "default"
    PREMITIVE = int | str | bool | float

    def __init__(self, client: 'DeepKeep'):
        self._client = client

    def _make_request(self, method: str = "GET", path: str = "", query_params: Union[dict, None] = None,
                      json_params: Union[dict, None] = None, headers: Union[dict[str, str], None] = None, **kwargs):
        query_params = query_params or {}
        json_params = json_params or {}
        headers = headers or {}

        res = requests.request(method=method, url=f"{self._client.base_url}/{path}",
                               json=json_params, params=query_params, headers={**self._client.auth_headers, **headers})

        if not res.ok:
            raise DeepkeepError(f"failed execution of method {self.__class__.__name__} with error code: {res.status_code} - "
                                f"{res.content}")

        return res.json()


@dataclass
class BaseData:
    def __init__(self, **kwargs):
        cls_fields = {field.name for field in fields(self)}
        for field in cls_fields:
            setattr(self, field, kwargs.get(field, self.__dataclass_fields__[field].default))

    def as_dict(self):
        return {key: value for key, value in asdict(self).items() if value is not None}
