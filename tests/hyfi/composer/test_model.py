from hyfi.composer.model import TestModel


def test_base_model():
    cfg = TestModel.save_hyfi_config(config_root="config")
    print(cfg)


if __name__ == "__main__":
    test_base_model()
