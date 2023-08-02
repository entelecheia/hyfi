from hyfi.runner.base import BaseRunner, TestRunner
from hyfi import HyFI


def test_runner() -> None:
    """Test runner"""
    BaseRunner.generate_config()
    TestRunner.generate_config(config_root="config")

    cfg = HyFI.compose("runner=__test__")
    cfg.calls = ["hello", "world"]
    print(cfg)
    HyFI.run_config(cfg)
    cfg.calls = [{"uses": "test", "with": {"a": 1, "b": 2}}]
    HyFI.run_config(cfg)


if __name__ == "__main__":
    test_runner()
