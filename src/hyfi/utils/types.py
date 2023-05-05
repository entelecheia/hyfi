from typing import Any, List, Sequence, Union

from omegaconf import ListConfig

IntSeq = Sequence[int]
ListLike = Union[ListConfig, List, Sequence[Any]]
