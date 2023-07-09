"""GPU utilities"""

import contextlib
import gc
import os
import time
from threading import Thread

from hyfi.utils.logging import LOGGING
from hyfi.utils.notebooks import NBs

logger = LOGGING.getLogger(__name__)

try:
    import GPUtil  # type: ignore
except ImportError:
    logger.debug("GPUtil not found. Please install it to use GPU utilities.")


class GPUMon(Thread):
    """Monitor GPU usage in a separate thread"""

    def __init__(self, delay=10, show_current_time=True, clear_output=True):
        super(GPUMon, self).__init__()
        self.stopped = False
        self.delay = delay  # Time between calls to GPUtil
        self.show_current_time = show_current_time
        self.clear_output = clear_output
        self.start()

    def run(self):
        while not self.stopped:
            if self.clear_output:
                NBs.clear_output()
            if self.show_current_time:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            GPUtil.showUtilization()
            time.sleep(self.delay)

    def stop(self):
        self.stopped = True

    @staticmethod
    def gpu_usage(all=False, attrList=None, useOldCode=False):
        return GPUtil.showUtilization(all=all, attrList=attrList, useOldCode=useOldCode)

    @staticmethod
    def get_gpus():
        return GPUtil.getGPUs()

    @staticmethod
    def get_gpu_info():
        gpus = GPUtil.getGPUs()
        return [
            {
                "id": gpu.id,
                "name": gpu.name,
                "load": gpu.load,
                "memory_used": gpu.memoryUsed,
                "memory_total": gpu.memoryTotal,
                "temperature": gpu.temperature,
            }
            for gpu in gpus
        ]

    @staticmethod
    def get_first_available(
        order="first",
        maxLoad=0.5,
        maxMemory=0.5,
        attempts=1,
        interval=900,
        verbose=False,
        includeNan=False,
        excludeID=None,
        excludeUUID=None,
    ):
        if excludeID is None:
            excludeID = []
        if excludeUUID is None:
            excludeUUID = []
        return GPUtil.getFirstAvailable(
            order=order,
            maxLoad=maxLoad,
            maxMemory=maxMemory,
            attempts=attempts,
            interval=interval,
            verbose=verbose,
            includeNan=includeNan,
            excludeID=excludeID,
            excludeUUID=excludeUUID,
        )

    @staticmethod
    def release_gpu_memory():
        gc.collect()
        with contextlib.suppress(ImportError):
            import torch  # type: ignore

            torch.cuda.empty_cache()


def nvidia_smi():
    """Run nvidia-smi and return the output as a string"""
    import subprocess

    return subprocess.run(["nvidia-smi", "-L"], stdout=subprocess.PIPE).stdout.decode(
        "utf-8"
    )


def is_cuda_available():
    """Check if cuda is available"""
    try:
        import torch  # type: ignore

        return torch.cuda.is_available()
    except ImportError:
        return False


class CudaDeviceNotFoundError(Exception):
    pass


def set_cuda(device=0):
    """Set cuda device to use"""
    try:
        import torch  # type: ignore

        _names = []
        if isinstance(device, str):
            device = device.replace("cuda:", "")
            ids = device.split(",")
        else:
            ids = [str(device)]
        for id in ids:
            _device_name = torch.cuda.get_device_name(int(id))
            _names.append(f"{_device_name} (id:{id})")
        logger.info(f"Setting cuda device to {_names}")
        device = ", ".join(ids)
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = device
    except ImportError as e:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        raise CudaDeviceNotFoundError("Cuda device not found") from e


class GPUs:
    ###############################
    # GPU Utility functions
    ###############################
    @staticmethod
    def nvidia_smi():
        return nvidia_smi()

    @staticmethod
    def set_cuda(device=0):
        return set_cuda(device)

    @staticmethod
    def gpu_usage(all=False, attrList=None, useOldCode=False):
        """
        Show GPU utilization in human readable format. This is a wrapper around the GPUtil library.

        Args:
                all: If True show all available GPUs ( default : False )
                attrList: List of attributes to show ( default : None )
                useOldCode: If True use old code instead of new code ( default : False )

        Returns:
                A string with the
        """
        try:
            from GPUtil import showUtilization  # type: ignore
        except ImportError:
            logger.error("GPUtil is not installed. To install, run: pip install GPUtil")
            return

        return showUtilization(all, attrList, useOldCode)
