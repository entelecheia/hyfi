import random
from pathlib import Path
from typing import Union

from datasets import Dataset

from hyfi.main import HyFI

logger = HyFI.getLogger(__name__)


def save_dataset_to_disk(
    data: Dataset,
    dataset_path: Union[str, Path],
) -> Dataset:
    """
    Save a dataset.
    """
    data.save_to_disk(dataset_path)
    logger.info("Dataset saved to %s.", dataset_path)

    return data


def load_dataset_from_disk(
    dataset_path: str,
    verbose: bool = False,
) -> Dataset:
    """
    Save a dataset.
    """
    data = Dataset.load_from_disk(dataset_path)
    logger.info("Dataset loaded from %s.", dataset_path)
    if verbose:
        print(data[0])
        print(data[-1])
        logger.info("Dataset features: %s", data.features)
        logger.info("Number of samples: %s", len(data))

    return data


def sample_dataset(
    data: Dataset,
    num_samples: int = 100,
    randomize: bool = True,
    random_seed: int = 42,
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
        print(data)

    return data
