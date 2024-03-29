from hyfi.composer import Composer
from hyfi.main import HyFI


def my_function():
    caller_module_name = HyFI.get_caller_module_name()
    print(f"The name of the caller module is {caller_module_name}")


def test_composer():
    my_function()
    cfg = Composer.compose("about", config_module="hyfi.conf")
    print(cfg)
    cfg = Composer.compose("/path/dirnames=__init__")
    print(cfg)


def test_composer_overrides():
    cfg = Composer.compose("about", overrides=["++about.name=test"])
    print(cfg)


def test_viewsource():
    Composer.viewsource("hyfi.about.AboutConfig")


if __name__ == "__main__":
    # test_composer()
    # test_composer_overrides()
    test_viewsource()
