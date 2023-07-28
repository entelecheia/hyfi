import random
from pathlib import Path
from typing import Optional, Union

from datasets.arrow_dataset import Dataset

from hyfi.main import HyFI

logger = HyFI.getLogger(__name__)


def save_dataset_to_disk(
    data: Dataset,
    dataset_path: Union[str, Path],
    verbose: bool = False,
    **kwargs,
) -> Dataset:
    """
    Save a dataset.
    """
    data.save_to_disk(str(dataset_path), **kwargs)
    logger.info("Dataset saved to %s.", dataset_path)
    if verbose:
        logger.info("Dataset features: %s", data.features)
        logger.info("Number of samples: %s", len(data))

    return data


def load_dataset_from_disk(
    dataset_path: str,
    num_heads: Optional[int] = 1,
    num_tails: Optional[int] = 1,
    verbose: bool = False,
) -> Dataset:
    """
    Save a dataset.
    """
    data = Dataset.load_from_disk(dataset_path)
    logger.info("Dataset loaded from %s.", dataset_path)
    if verbose:
        if num_heads:
            num_heads = min(num_heads, len(data))
            print(data[:num_heads])
        if num_tails:
            num_tails = min(num_tails, len(data))
            print(data[-num_tails:])
        logger.info("Dataset features: %s", data.features)
        logger.info("Number of samples: %s", len(data))

    return data


def sample_dataset(
    data: Dataset,
    num_samples: int = 100,
    randomize: bool = True,
    random_seed: int = 42,
    num_heads: Optional[int] = 1,
    num_tails: Optional[int] = 1,
    verbose: bool = False,
) -> Dataset:
    """
    Sample a dataset.
    """
    if random_seed > 0:
        random.seed(random_seed)
    if randomize:
        idx = random.sample(range(len(data)), num_samples)
    else:
        idx = range(num_samples)

    data = data.select(idx)
    logger.info("Sampling done.")
    if verbose:
        if num_heads:
            num_heads = min(num_heads, len(data))
            print(data[:num_heads])
        if num_tails:
            num_tails = min(num_tails, len(data))
            print(data[-num_tails:])

    return data
