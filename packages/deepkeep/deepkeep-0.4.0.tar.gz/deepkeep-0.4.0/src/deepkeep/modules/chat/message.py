from dataclasses import dataclass
from typing import Union
from time import sleep

from deepkeep._exceptions import DeepkeepError
from ..base_module import BaseModule, BaseData

__all__ = ["Message"]


@dataclass
class MessageData(BaseData):
    content: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Message(BaseModule):
    root_path: str = "pipeline"

    def create(self, conversation_id: str, host_id: str = BaseModule._DEFAULT_HOST_,
               content: Union[MessageData, dict, str, None] = None, user_id: Union[str, None] = None,
               verbose: bool = False):
        additional_details = {}
        content = content or MessageData()

        if isinstance(content, dict):
            content = MessageData(**content)
        elif isinstance(content, str):
            content = MessageData(content=content)
        elif not isinstance(content, MessageData):
            raise DeepkeepError("input content is not valid. should be one of the following type: "
                                "\n\tdeepkeep.modules.Message | dict | str")

        if user_id and isinstance(user_id, str):
            additional_details = {
                "headers": {
                    "user": user_id
                }
            }

        _res = self._make_request(method="POST", path=f"{self.root_path}/{host_id}/chat/{conversation_id}/message",
                                  json_params=content.as_dict(), **additional_details)

        if _res and verbose:
            request_id = _res.get("request_id")

            # TODO: fix and beautify retry
            # get extra data
            for _retry in range(5):
                try:
                    sleep(0.5)
                    _res_verbose = self._make_request(path=f"report/stats/message/{request_id}",
                                                      **additional_details)

                    _res |= {"statistics": _res_verbose}
                    break
                except DeepkeepError as verbose_error:
                    _res |= {"statistics": {"error": verbose_error}}

        return _res

    def get(self, conversation_id: str, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/chat/{conversation_id}/messages")

    def stats(self, request_id: str):
        return self._make_request(path=f"report/stats/message/{request_id}")
