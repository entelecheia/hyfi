from pydantic import BaseModel

from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


class ModuleConfig(BaseModel):
    """Module Configuration"""

    library_dir: str = ""
    modules: list = None
