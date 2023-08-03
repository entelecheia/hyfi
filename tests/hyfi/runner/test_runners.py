from hyfi.runner.base import BaseRunner, TestRunner
from hyfi import HyFI


def test_runner() -> None:
    """Test runner"""
    print(BaseRunner.generate_config())
    print(TestRunner().load_args.kwargs)
    cfg = HyFI.compose("runner=__test__")
    cfg.calls = ["hello", "world"]
    print(cfg)
    HyFI.run_config(cfg)
    cfg.calls = [{"uses": "test", "with": {"a": 1, "b": 2}}]
    HyFI.run_config(cfg)


def test_runner_config() -> None:
    """Test runner"""
    print(TestRunner.generate_config(config_root="config"))


if __name__ == "__main__":
    test_runner()
    test_runner_config()
