from hyfi.run import Run


def test_run_config():
    print(Run().generate_config())
    cfg = Run(_target_="hyfi.HyFI.run", a=1, b=2)
    # print(cfg._config_name_, cfg._config_group_)
    # print(cfg.kwargs)
    print(cfg.generate_config(save=False))
    print(Run(_config_name_="load_data").generate_config(save=False))
    print(Run(_config_name_="load_data").kwargs)


if __name__ == "__main__":
    test_run_config()
