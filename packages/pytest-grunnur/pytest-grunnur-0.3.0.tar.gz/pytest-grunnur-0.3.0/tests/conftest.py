import pytest
from grunnur.testing import MockBackendFactory

# Cannot just use the plugin directly since it is loaded before the coverage plugin,
# and all the function definitions in all `grunnur` modules get marked as not covered.
from pytest_grunnur.plugin import (
    api,  # noqa: F401
    context,  # noqa: F401
    device,  # noqa: F401
    multi_device_context,  # noqa: F401
    multi_device_set,  # noqa: F401
    platform,  # noqa: F401
    some_context,  # noqa: F401
    some_device,  # noqa: F401
)
from pytest_grunnur.plugin import pytest_addoption as grunnur_pytest_addoption
from pytest_grunnur.plugin import pytest_generate_tests as grunnur_pytest_generate_tests
from pytest_grunnur.plugin import pytest_report_header as grunnur_pytest_report_header


@pytest.fixture
def mock_backend_factory(monkeypatch):
    return MockBackendFactory(monkeypatch)


def pytest_generate_tests(metafunc):
    grunnur_pytest_generate_tests(metafunc)


def pytest_addoption(parser):
    grunnur_pytest_addoption(parser)


def pytest_report_header(config):
    grunnur_pytest_report_header(config)
