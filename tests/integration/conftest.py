import pytest


def pytest_collection_modifyitems(config, items):
    # skip all integration tests if not explicitly requested
    if not config.option.integration:
        skip_integration = pytest.mark.skip(reason="need --integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


@pytest.fixture(scope="session")
def project(request):
    """Return the GCP project name for integration tests."""
    project = request.config.getoption("--project")

    if not project:
        # skip all tests that require a project name
        pytest.skip("missing --project option")

    return request.config.getoption("--project")
