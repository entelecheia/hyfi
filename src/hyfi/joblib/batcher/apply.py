#!python
from __future__ import absolute_import, division, print_function, with_statement

from typing import Any, Callable, Mapping, Optional, Sequence

import pandas as pd

from .batcher import Batcher


def decorator_apply(
    func: Callable,
    batcher: Optional[Batcher] = None,
    cache: Optional[int] = None,
    vectorize: Optional[Callable] = None,
    description: str = "batch_apply",
):
    """
    Decorator that applies a function to each row of a minibatch.

    Args:
        func: The function to apply.
        batcher: The batcher to use for processing the minibatches.
        cache: The maximum size of the LRU cache for the function.
        vectorize: The function to use for vectorization.
        description: The description of the apply operation.

    Returns:
        The wrapper function.
    """

    def wrapper_func(*args, **kwargs):
        return Apply(
            func,
            args=args[1:],
            kwargs=kwargs,
            batcher=batcher,
            cache=cache,
            vectorize=vectorize,
            description=description,
        ).transform(args[0])

    return wrapper_func


def batch_transform(args):
    """
    Applies a function to each row of a minibatch.

    Args:
        args: A tuple containing the following elements:
            - data: The data to apply the function to.
            - func: The function to apply.
            - func_args: The arguments to pass to the function.
            - func_kwargs: The keyword arguments to pass to the function.
            - cache_maxsize: The maximum size of the LRU cache for the function.
            - vectorize_func: The function to use for vectorization.

    Returns:
        The result of applying the function to the data.
    """
    data = args[0]
    func = args[1]
    func_args = args[2]
    func_kwargs = args[3]
    cache_maxsize = args[4]
    vectorize_func = args[5]
    if vectorize_func is not None:
        from numba import vectorize

        return vectorize(vectorize_func, fastmath=True)(func)(*zip(*data))
    if cache_maxsize is not None:
        from functools import lru_cache

        func = lru_cache(maxsize=cache_maxsize)(func)
    # Applying per DataFrame row is very slow, use ApplyBatch instead
    if isinstance(data, pd.DataFrame):
        return data.apply(lambda x: func(x, *func_args, **func_kwargs), axis=1)
    elif isinstance(data, pd.Series):
        return data.apply(lambda x: func(x, *func_args, **func_kwargs))
    return [func(row, *func_args, **func_kwargs) for row in data]


class Apply(object):
    """
    Applies a function to each row of a minibatch.

    Args:
        function: The function to apply.
        batcher: The batcher to use for processing the minibatches.
        args: The arguments to pass to the function.
        kwargs: The keyword arguments to pass to the function.
        cache: The maximum size of the LRU cache for the function.
        vectorize: The function to use for vectorization.
        description: The description of the apply operation.

    Attributes:
        batcher: The batcher to use for processing the minibatches.
        function: The function to apply.
        args: The arguments to pass to the function.
        kwargs: The keyword arguments to pass to the function.
        cache: The maximum size of the LRU cache for the function.
        vectorize: The function to use for vectorization.
        description: The description of the apply operation.
    """

    def __init__(
        self,
        function: Callable,
        batcher: Optional[Batcher] = None,
        args: Optional[Sequence] = None,
        kwargs: Optional[Mapping] = None,
        cache: Optional[int] = None,
        vectorize: Optional[Callable] = None,
        description: str = "batch_apply",
    ):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.batcher = Batcher() if batcher is None else batcher
        self.function = function
        self.args = [args]
        self.kwargs = [kwargs]
        self.cache = [cache]
        self.vectorize = [vectorize]
        self.description = description

    def fit(self, **kwargs):
        """
        Fit the apply operation.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            The apply operation.
        """
        return self

    def fit_transform(
        self,
        data: Any,
        input_split: bool = False,
        merge_output: bool = True,
        minibatch_size: Optional[int] = None,
        batcher: Optional[Batcher] = None,
    ):
        """
        Fit and transform the apply operation.

        Args:
            data: The data to apply the function to.
            input_split: Whether to split the input data into minibatches.
            merge_output: Whether to merge the output of the minibatches.
            minibatch_size: The size of the minibatches.
            batcher: The batcher to use for processing the minibatches.

        Returns:
            The result of applying the function to the data.
        """
        return self.transform(data, input_split, merge_output, minibatch_size, batcher)

    def transform(
        self,
        data: Any,
        input_split: bool = False,
        merge_output: bool = True,
        minibatch_size: Optional[int] = None,
        batcher: Optional[Batcher] = None,
    ):
        """
        Transform the apply operation.

        Args:
            data: The data to apply the function to.
            input_split: Whether to split the input data into minibatches.
            merge_output: Whether to merge the output of the minibatches.
            minibatch_size: The size of the minibatches.
            batcher: The batcher to use for processing the minibatches.

        Returns:
            The result of applying the function to the data.
        """
        if batcher is None:
            batcher = self.batcher
        return batcher.process_batches(
            batch_transform,
            data,
            [self.function] + self.args + self.kwargs + self.cache + self.vectorize,
            input_split=input_split,
            merge_output=merge_output,
            minibatch_size=minibatch_size,
            description=self.description,
        )
