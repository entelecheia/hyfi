from typing import Any, List, Optional

from hyfi.composer import BaseModel
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class ModuleConfig(BaseModel):
    """Module Configuration"""

    library_dir: str = ""
    modules: Optional[List[Any]] = None
