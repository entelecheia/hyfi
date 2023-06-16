"""HyFI: Hydra Fast Interface (Hydra and Pydantic based interface framework)"""
from hyfi.__cli__ import hydra_main
from hyfi.__global__ import __about__ as about
from hyfi.__global__ import __hydra_version_base__
from hyfi.__global__.config import __global_config__ as global_config
from hyfi.main import HyFI
from hyfi.main import HyFI as H
from hyfi.main import HyFI as HI
from hyfi.utils.logging import getLogger
