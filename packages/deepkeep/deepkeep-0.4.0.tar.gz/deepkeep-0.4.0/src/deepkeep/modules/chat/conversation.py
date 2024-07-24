from dataclasses import dataclass
from typing import Union

from ..base_module import BaseModule, BaseData

__all__ = ["Conversation"]


@dataclass
class ConversationData(BaseData):
    title: str = "New Chat"
    user_name: Union[str, None] = None
    system_prompt: Union[str, None] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Conversation(BaseModule):
    root_path: str = "pipeline"

    def create(self, user_id: str, host_id: str = BaseModule._DEFAULT_HOST_,
               data: Union[ConversationData, dict, None] = None, **kwargs):
        if not data or isinstance(data, dict):
            data = kwargs | (data or {})
            data = ConversationData(**data)

        return self._make_request(method="POST", path=f"{self.root_path}/{host_id}/chat/conversation",
                                  headers={"user": user_id}, json_params=data.as_dict())

    def get(self, conversation_id: str, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/chat/{conversation_id}")

    def delete(self, conversation_id: str, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(method="DELETE", path=f"{self.root_path}/{host_id}/chat/{conversation_id}")

    def update(self, conversation_id: str, data: Union[ConversationData, dict],
               host_id: str = BaseModule._DEFAULT_HOST_):
        data = data or ConversationData()
        if isinstance(data, dict):
            data = ConversationData(**data)

        return self._make_request(method="PUT", path=f"{self.root_path}/{host_id}/chat/{conversation_id}",
                                  json_params=data.as_dict())

    def stats(self, conversation_id: str):
        return self._make_request(path=f"report/stats/conversation/{conversation_id}")
