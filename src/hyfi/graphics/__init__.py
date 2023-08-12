from .collage import COLLAGE, Collage
from .motion import MOTION
from .utils import GUTILs


class GRAPHICs(COLLAGE, MOTION, GUTILs):
    def __init__(self):
        pass


__all__ = ["GRAPHICs", "COLLAGE", "MOTION", "GUTILs", "Collage"]
