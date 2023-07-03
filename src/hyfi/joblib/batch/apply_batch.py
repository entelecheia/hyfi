from __future__ import absolute_import, division, print_function, with_statement

from typing import Any, Callable, Mapping, Optional, Sequence

from .batcher import Batcher


def decorator_apply_batch(
    func: Callable,
    batcher: Optional[Batcher] = None,
):
    """
    A decorator that applies a function to a minibatch.

    Args:
        func (Callable): The function to apply to the minibatch.
        batcher (Optional[Batcher], optional): The batcher to use. Defaults to None.

    Returns:
        Callable: The decorated function.
    """

    def wrapper_func(*args, **kwargs):
        return ApplyBatch(
            func, args=args[1:], kwargs=kwargs, batcher=batcher
        ).transform(args[0])

    return wrapper_func


class ApplyBatch(object):
    """
    Applies a function to the entire minibatch. Use this for example on Pandas dataframes, to avoid per-row overhead.
    Function needs to be applicable to the array/list of values!
    If not, modify/wrap the function to process a list, or use Apply
    """

    def __init__(
        self,
        function: Callable,
        batcher: Optional[Batcher] = None,
        args: Optional[Sequence] = None,
        kwargs: Optional[Mapping] = None,
    ):
        """
        Initializes an instance of ApplyBatch.

        Args:
            function (Callable): The function to apply to the minibatch.
            batcher (Optional[Batcher], optional): The batcher to use. Defaults to None.
            args (Optional[Sequence], optional): Additional positional arguments to pass to the function. Defaults to None.
            kwargs (Optional[Mapping], optional): Additional keyword arguments to pass to the function. Defaults to None.
        """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.batcher = Batcher() if batcher is None else batcher
        self.function = function
        self.args = [args]
        self.kwargs = [kwargs]

    def fit(self, **kwargs):
        """
        Fits the model.

        Args:
            **kwargs: Additional keyword arguments to pass to the function.

        Returns:
            self: The instance of ApplyBatch.
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
        Fits the model and applies the function to the minibatch.

        Args:
            data (Any): The data to apply the function to.
            input_split (bool, optional): Whether to split the input data into minibatches. Defaults to False.
            merge_output (bool, optional): Whether to merge the output of the minibatches. Defaults to True.
            minibatch_size (Optional[int], optional): The size of the minibatches. Defaults to None.
            batcher (Optional[Batcher], optional): The batcher to use. Defaults to None.

        Returns:
            Any: The output of the function applied to the minibatch.
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
        Applies the function to the minibatch.

        Args:
            data (Any): The data to apply the function to.
            input_split (bool, optional): Whether to split the input data into minibatches. Defaults to False.
            merge_output (bool, optional): Whether to merge the output of the minibatches. Defaults to True.
            minibatch_size (Optional[int], optional): The size of the minibatches. Defaults to None.
            batcher (Optional[Batcher], optional): The batcher to use. Defaults to None.

        Returns:
            Any: The output of the function applied to the minibatch.
        """
        if batcher is None:
            batcher = self.batcher
        return batcher.process_batches(
            task=batch_transform,
            data=data,
            args=[self.function] + self.args + self.kwargs,
            input_split=input_split,
            merge_output=merge_output,
            minibatch_size=minibatch_size,
        )


def batch_transform(args):
    """
    Applies a function to a minibatch.

    Args:
        args: The arguments to pass to the function.

    Returns:
        Any: The output of the function applied to the minibatch.
    """
    data = args[0]
    func = args[1]
    func_args = args[2]
    func_kwargs = args[3]
    return func(data, *func_args, **func_kwargs)
