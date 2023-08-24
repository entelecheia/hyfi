from hyfi.composer import DocGenerator


def test_docs_generate_configs():
    DocGenerator.generate_config()
    dg = DocGenerator()
    dg.generate_config_docs()


def test_docs_generate_refs():
    DocGenerator.generate_config()
    dg = DocGenerator()
    dg.generate_reference_docs()


if __name__ == "__main__":
    # test_docs_generate_configs()
    test_docs_generate_refs()
