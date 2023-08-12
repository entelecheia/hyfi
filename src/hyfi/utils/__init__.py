from .cached import CACHED
from .conf import CONFs
from .datasets import DATASETs
from .envs import ENVs
from .funcs import FUNCs
from .gpumon import GPUs
from .iolibs import IOLIBs
from .logging import LOGGING
from .notebooks import NBs
from .packages import PKGs
from .safeeval import SAFEEVAL, SafeEval


class UTILs(
    CACHED,
    CONFs,
    DATASETs,
    ENVs,
    FUNCs,
    GPUs,
    IOLIBs,
    LOGGING,
    NBs,
    PKGs,
    SAFEEVAL,
):
    def __init__(self) -> None:
        raise NotImplementedError("Use one of the static construction functions")


__all__ = [
    "CONFs",
    "DATASETs",
    "ENVs",
    "FUNCs",
    "GPUs",
    "IOLIBs",
    "LOGGING",
    "NBs",
    "PKGs",
    "UTILs",
    "SAFEEVAL",
    "SafeEval",
]
