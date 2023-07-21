from hyfi.composer import Composer

import inspect


def my_function():
    caller_module = inspect.getmodule(inspect.stack()[1][0])
    caller_module_name = caller_module.__name__
    print(f"The name of the caller module is {caller_module_name}")


def test_composer():
    cfg = Composer._compose("about", config_module="hyfi.conf")
    print(cfg)


if __name__ == "__main__":
    my_function()
    test_composer()
