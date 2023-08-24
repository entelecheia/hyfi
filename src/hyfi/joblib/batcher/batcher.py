"""Batcher class for handling parallel jobs on minibatches"""
import contextlib
import multiprocessing
from contextlib import closing
from math import ceil
from typing import Any, Callable, List, Optional

import pandas as pd
import scipy.sparse as ssp
from tqdm.auto import tqdm

from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class Batcher(object):
    """Scheduler to handle parallel jobs on minibatches

    Attributes:
        procs (int):
                Number of process(es)/thread(s) for executing task in parallel. Used for multiprocessing, threading and Loky

        minibatch_size (int):
                Expected size of each minibatch

        backend (str): {'serial', 'multiprocessing', 'threading', 'loky', 'spark', 'dask', 'ray'}
                Backend for computing the tasks

                        - 'serial' sequential execution without a backend scheduler

                        - 'multiprocessing' Python standard multiprocessing library

                        - 'threading' Python standard threading library

                        - 'loky' Loky fork of multiprocessing library

                        - 'joblib' Joblib fork of multiprocessing library

                        - 'ray' Ray local or distributed execution

        task_num_cpus (int):
                Number of CPUs to reserve per minibatch task for Ray

        task_num_gpus (int):
                Number of GPUs to reserve per minibatch task for Ray

        backend_handle (object):
                Backend handle for sending tasks

        verbose (int):
                Verbosity level.
                Setting verbose > 0 will display additional information depending on the specific level set.
    """

    def __init__(
        self,
        procs: Optional[int] = 0,
        minibatch_size: int = 20000,
        backend_handle: Any = None,
        backend: str = "multiprocessing",
        task_num_cpus: int = 1,
        task_num_gpus: int = 0,
        verbose: int = 0,
    ):
        if procs == 0 or procs is None:
            procs = multiprocessing.cpu_count()
        self.procs = procs
        self.verbose = verbose
        self.minibatch_size = minibatch_size
        self.backend_handle = backend_handle
        self.backend = backend
        self.task_num_cpus = task_num_cpus
        self.task_num_gpus = task_num_gpus

    def split_batches(
        self,
        data: Any,
        minibatch_size: Optional[int] = None,
        backend: Any = None,
    ):
        """Split data into minibatches with a specified size

        Arguments:
            data (list, tuple, dict, numpy.ndarray, scipy.sparse.csr_matrix, pandas.DataFrame):
                List-like data to be split into batches. Includes numpy matrices and Pandas DataFrames.

            minibatch_size (int):
                Expected sizes of minibatches split from the data.

            backend (str):
                Backend to use, instead of the Batcher backend attribute

        Returns:
            data_split (list):
                List of minibatches, each entry is a list-like object representing the data subset in a batch.
        """
        if minibatch_size is None:
            minibatch_size = self.minibatch_size
        if backend is None:
            backend = self.backend
        if isinstance(data, (list, tuple, dict)):
            len_data = len(data)
        else:
            len_data = data.shape[0]

        if isinstance(data, pd.DataFrame):
            data = [
                data.iloc[x * minibatch_size : (x + 1) * minibatch_size]
                for x in range(int(ceil(len_data / minibatch_size)))
            ]
        elif isinstance(data, dict):
            data = [
                dict(
                    list(data.items())[
                        x * minibatch_size : min(len_data, (x + 1) * minibatch_size)
                    ]
                )
                for x in range(int(ceil(len_data / minibatch_size)))
            ]
        else:
            data = [
                data[x * minibatch_size : min(len_data, (x + 1) * minibatch_size)]
                for x in range(int(ceil(len_data / minibatch_size)))
            ]
        return data

    def collect_batches(self, data: Any, backend: Any = None):
        if backend is None:
            backend = self.backend
        return data

    def merge_batches(self, data: Any):
        """Merge a list of data minibatches into one single instance representing the data

        Arguments:
            data (list):
                List of minibatches to merge

        Returns:
            data (list, numpy.ndarray, scipy.sparse.csr_matrix, pandas.DataFrame):
                Single complete list-like data merged from given batches
        """
        print(data)
        if isinstance(data[0], ssp.csr_matrix):  # type: ignore
            return ssp.vstack(data)  # type: ignore
        if isinstance(data[0], (pd.DataFrame, pd.Series)):
            return pd.concat(data)
        return [item for sublist in data for item in sublist]

    def process_batches(
        self,
        task: Callable,
        data: Any,
        args: List[Any],
        backend: Optional[str] = None,
        backend_handle: Any = None,
        input_split: bool = False,
        merge_output: bool = True,
        minibatch_size: Optional[int] = None,
        procs: Optional[int] = None,
        task_num_cpus: Optional[int] = None,
        task_num_gpus: Optional[int] = None,
        verbose: Optional[int] = None,
        description: str = "batch_apply",
    ):
        """
        Apply a function on minibatches of data in parallel

        Arguments:
            task (callable):
                Function to apply on each minibatch with other specified arguments

            data (list, tuple, dict, numpy.ndarray, scipy.sparse.csr_matrix, pandas.DataFrame):
                Samples to split into minibatches and apply the specified function on

            args (list):
                Arguments to pass to the specified function following the mini-batch

            input_split (bool):
                If True, input data is already mapped into minibatches, otherwise data will be split on call.

            merge_output (bool):
                If True, results from minibatches will be reduced into one single instance before return.

            procs (int):
                Number of process(es)/thread(s) for executing task in parallel. Used for multiprocessing, threading, Loky and Ray

            minibatch_size (int):
                Expected size of each minibatch

            backend (str): {'serial', 'multiprocessing', 'threading', 'loky', 'spark', 'dask', 'ray'}
                Backend for computing the tasks

                        - 'serial' sequential execution without a backend scheduler

                        - 'multiprocessing' Python standard multiprocessing library

                        - 'threading' Python standard threading library

                        - 'loky' Loky fork of multiprocessing library

                        - 'joblib' Joblib fork of multiprocessing library

                        - 'ray' Ray local or distributed execution

            backend_handle (object):
                Backend handle for sending tasks

            task_num_cpus (int):
                Number of CPUs to reserve per minibatch task for Ray

            task_num_gpus (int):
                Number of GPUs to reserve per minibatch task for Ray

            verbose (int):
                Verbosity level.
                Setting verbose > 0 will display additional information depending on the specific level set.

        Returns:
            data (list):
                If merge_output is specified as True, this will be a list-like object representing
                the dataset, with each entry as a sample. Otherwise this will be a list of list-like
                objects, with each entry representing the results from a minibatch.
        """
        if procs is None:
            procs = self.procs
        if backend is None:
            backend = self.backend
        if backend_handle is None:
            backend_handle = self.backend_handle
        if task_num_cpus is None:
            task_num_cpus = self.task_num_cpus
        if task_num_gpus is None:
            task_num_gpus = self.task_num_gpus
        if verbose is None:
            verbose = self.verbose
        # if verbose > 1:
        logger.debug(
            "backend: %s, minibatch_size: %s, procs: %s, input_split: %s, merge_output: %s, len(data): %s, len(args): %s",
            backend,
            self.minibatch_size,
            procs,
            input_split,
            merge_output,
            len(data),
            len(args),
        )

        # if verbose > 10:
        logger.debug(
            " len(data): %s len(args): %s [type(x) for x in data]: %s [type(x) for x in args]: %s",
            len(data),
            len(args),
            [type(x) for x in data],
            [type(x) for x in args],
        )

        if not (input_split):
            paral_params = [
                [data_batch] + args
                for data_batch in self.split_batches(data, minibatch_size)
            ]
        else:
            paral_params = [[data_batch] + args for data_batch in data]
        logger.debug("Start task, len(paral_params): %s", len(paral_params))
        results = []
        if backend == "serial":
            results = [
                task(minibatch) for minibatch in tqdm(paral_params, desc=description)
            ]
        else:
            if backend == "multiprocessing":
                with closing(
                    multiprocessing.Pool(max(1, procs), maxtasksperchild=2)
                ) as pool:
                    results = pool.map_async(task, paral_params)
                    pool.close()
                    pool.join()
                    results = results.get()
            elif backend == "threading":
                with closing(multiprocessing.Pool(max(1, procs))) as pool:
                    results = pool.map(task, paral_params)
                    pool.close()
                    pool.join()
            elif backend == "loky":
                from loky import get_reusable_executor

                pool = get_reusable_executor(max_workers=max(1, procs))
                results = list(pool.map(task, tqdm(paral_params, desc=description)))
            elif backend == "joblib":
                from joblib import Parallel, delayed

                with tqdm_joblib(
                    tqdm(desc=description, total=len(paral_params))
                ) as pbar:
                    results = Parallel(n_jobs=procs)(
                        delayed(task)(params) for params in paral_params
                    )
            elif backend == "p_tqdm":
                from p_tqdm import p_map

                results = p_map(task, paral_params, num_cpus=procs)
            elif backend == "ray":

                @self.backend_handle.remote(
                    num_cpus=task_num_cpus, num_gpus=task_num_gpus
                )
                def f_ray(f, data):
                    return f(data)

                pbar = tqdm(desc=description, total=len(paral_params) + 1)
                results = [
                    f_ray.remote(task, paral_params.pop(0))
                    for _ in range(min(len(paral_params), self.procs))
                ]
                uncompleted = results
                pbar.update(len(results))
                while paral_params:
                    # More tasks than available processors. Queue the task calls
                    done, remaining = self.backend_handle.wait(
                        uncompleted, timeout=60, fetch_local=False
                    )
                    # if verbose > 5:  print("Done, len(done), len(remaining)", len(done), len(remaining))
                    if len(done) == 0:
                        continue
                    done = done[0]
                    uncompleted = [x for x in uncompleted if x != done]
                    if len(remaining) > 0:
                        new = f_ray.remote(task, paral_params.pop(0))
                        pbar.update(1)
                        uncompleted.append(new)
                        results.append(new)
                results = [self.backend_handle.get(x) for x in results]
                pbar.update(1)
                pbar.close()

        if merge_output:
            return self.merge_batches(self.collect_batches(results, backend=backend))
        logger.debug(
            "Task: %s  backend: %s  backend_handle: %s completed",
            task,
            backend,
            backend_handle,
        )
        return results

    def __getstate__(self):
        return dict(self.__dict__.items())

    def __setstate__(self, params: dict):
        for key in params:
            setattr(self, key, params[key])


@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""
    import joblib

    class TqdmBatchCompletionCallBack(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallBack
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


# from joblib import Parallel, delayed

# with tqdm_joblib(tqdm(desc="My calculation", total=10)) as progress_bar:
#     Parallel(n_jobs=16)(delayed(sqrt)(i**2) for i in range(10))
