from typing import Union
from ..base_module import BaseModule

__all__ = ["Assessment"]


class Assessment(BaseModule):
    root_path: str = "assessment"

    def create(self, model: str, report_types: Union[str, list[str]], **kwargs):
        if isinstance(report_types, str):
            report_types = [report_types]

        return self._make_request(method="POST", path=f"{self.root_path}/llm/run",
                                  json_params={
                                      "model": model,
                                      "report_types": report_types,
                                      **kwargs
                                  })

    def status(self, request_id: str = None):
        if request_id:
            return self._make_request(path=f"{self.root_path}/llm/{request_id}/status")

        return self._make_request(path=f"{self.root_path}/llm/")

    def list_pipelines(self):
        return {
            "models": self._make_request(path=f"{self.root_path}/llm/models/list"),
            "report_types": self._make_request(path=f"{self.root_path}/llm/reports/list")
        }
