#!python
from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
import pandas as pd
from .batcher import Batcher

# from tqdm.auto import tqdm


def decorator_apply(
    func, batcher=None, cache=None, vectorize=None, description="batch_apply"
):
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
    f = args[1]
    f_args = args[2]
    f_kwargs = args[3]
    if args[5] is not None:
        from numba import vectorize

        return vectorize(args[5], fastmath=True)(f)(*zip(*args[0]))
    if args[4] is not None:
        from functools import lru_cache

        f = lru_cache(maxsize=args[4])(f)
    # Applying per DataFrame row is very slow, use ApplyBatch instead
    if isinstance(args[0], pd.DataFrame):
        return args[0].apply(lambda x: f(x, *f_args, **f_kwargs), axis=1)
    elif isinstance(args[0], pd.Series):
        return args[0].apply(lambda x: f(x, *f_args, **f_kwargs))
    return [f(row, *f_args, **f_kwargs) for row in args[0]]


class Apply(object):
    # Applies a function to each row of a minibatch
    def __init__(
        self,
        function,
        batcher=None,
        args=[],
        kwargs={},
        cache=None,
        vectorize=None,
        description="batch_apply",
    ):
        if batcher is None:
            self.batcher = Batcher()
        else:
            self.batcher = batcher
        self.function = function
        self.args = [args]
        self.kwargs = [kwargs]
        self.cache = [cache]
        self.vectorize = [vectorize]
        self.description = description

    def fit(self, data, input_split=False, batcher=None):
        return self

    def fit_transform(
        self,
        data,
        input_split=False,
        merge_output=True,
        minibatch_size=None,
        batcher=None,
    ):
        return self.transform(data, input_split, merge_output, minibatch_size, batcher)

    def transform(
        self,
        data,
        input_split=False,
        merge_output=True,
        minibatch_size=None,
        batcher=None,
    ):
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


# import wordbatch.batcher as batcher
# b= batcher.Batcher(minibatch_size=2)#, method="serial")
# import numpy as np
# a= Apply(np.power, b, [2],{})
# print(a.transform([1, 2, 3, 4]))
