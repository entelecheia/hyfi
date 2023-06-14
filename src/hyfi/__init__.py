"""HyFI: Hydra Fast Interface (Hydra and Pydantic based interface framework)"""
from hyfi.__cli__ import getLogger, hydra_main
from hyfi.env import __about__ as about
from hyfi.env import __global_config__ as global_config
from hyfi.env import __hydra_version_base__
from hyfi.main import HyFI
from hyfi.main import HyFI as H
from hyfi.main import HyFI as HI
