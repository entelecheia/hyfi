from hyfi.joblib.batcher.apply import Apply
from hyfi.joblib.batcher.apply_batch import ApplyBatch
from hyfi.joblib import JobLib


def batcher_test(backend):
    print(f"Testing backend: {backend}")
    joblib = JobLib(backend=backend, num_workers=2, minibatch_size=2)
    # b = Batcher(minibatch_size=2, backend=backend, procs=2)
    joblib.initialize()
    b = joblib._batcher_instance_
    import numpy as np

    a = Apply(np.power, b, [2], {})
    print(a.transform([1, 2, 3, 4]))
    a = ApplyBatch(np.power, b, [2], {})
    print(a.transform([1, 2, 3, 4]))


def test_bacher_backends():
    backends = ["serial", "threading", "multiprocessing", "joblib"]
    # sourcery skip: no-loop-in-tests
    for backend in backends:
        batcher_test(backend)


if __name__ == "__main__":
    test_bacher_backends()
