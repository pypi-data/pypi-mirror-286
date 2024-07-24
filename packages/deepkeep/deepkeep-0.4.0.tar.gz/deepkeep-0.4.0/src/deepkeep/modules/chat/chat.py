from deepkeep._exceptions import DeepkeepError
from ..base_module import BaseModule

__all__ = ["Chat"]


class Chat(BaseModule):
    root_path: str = "pipeline"

    def create(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(method="POST", path=f"{self.root_path}/{host_id}/chat")

    def delete(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(method="DELETE", path=f"{self.root_path}/{host_id}/chat")

    def get(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/chat")

    def stats(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"report/stats/chat/{host_id}")

    def status(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/status")

    def get_config(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/config")

    def set_config(self, host_id: str = BaseModule._DEFAULT_HOST_, pipeline: dict | None = None):
        if not pipeline:
            raise DeepkeepError("pipeline is required and not specified")

        return self._make_request(method="PUT", path=f"{self.root_path}/{host_id}/config", json_params=pipeline)

    def list_pipelines(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/pipelines/list")
