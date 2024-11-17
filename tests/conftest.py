def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )

    parser.addoption(
        "--project",
        type=str,
        help="gcp project name for integration tests",
    )
