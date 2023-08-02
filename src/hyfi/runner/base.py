from typing import List, Optional

from hyfi.composer import BaseModel


class BaseRunner(BaseModel):
    _config_group_: str = "runner"
    _config_name_: str = "__init__"

    calls: Optional[List[str]] = None

    def __call__(self) -> None:
        self.run()

    def run(self):
        raise NotImplementedError
