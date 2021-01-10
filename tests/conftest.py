def pytest_addoption(parser):
    parser.addoption("--api-key")


def pytest_generate_tests(metafunc):
    metafunc.parametrize("api_key", [(metafunc.config.getoption("--api-key"))])
