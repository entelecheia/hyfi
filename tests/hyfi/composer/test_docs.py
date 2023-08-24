from hyfi.composer import DocGenerator


def test_generate_configs():
    DocGenerator.generate_config()
    DocGenerator.generate_config()


def test_generate_docs():
    dg = DocGenerator()
    dg.generate_config_docs()
    dg.generate_reference_docs()


if __name__ == "__main__":
    test_generate_configs()
    test_generate_docs()
