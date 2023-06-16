from pydantic import BaseModel

from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


class ModuleConfig(BaseModel):
    """Module Configuration"""

    library_dir: str = ""
    modules: list = []
