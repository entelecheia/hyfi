from hyfi.composer.model import TestModel, InnerTestModel


def test_base_model():
    cfg = TestModel.generate_config(config_root="config")
    print(cfg)
    cfg = TestModel().generate_config(config_root="config")
    print(cfg)
    cfg = InnerTestModel.generate_config(config_root="config")
    print(cfg)


if __name__ == "__main__":
    test_base_model()
