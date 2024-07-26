from collections.abc import Iterable
from functools import lru_cache, reduce
from typing import Any, TypeVar, cast

import pytest
from grunnur import API, Context, Device, DeviceFilter, Platform, PlatformFilter, all_api_ids


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Adds the following command-line options:

    * ``--api``: select a specific API to test (out of returned by :py:func:`grunnur.all_api_ids`).
    * ``--platform-include-mask``: run tests only on platforms whose names matches the mask.
    * ``--platform-exclude-mask``: exclude platforms whose names matches the mask from the tests.
    * ``--device-include-mask``: run tests only on devices whose names matches the mask.
    * ``--device-exclude-mask``: exclude devices whose names matches the mask from the tests.
    * ``--include-duplicate-devices``: if there are devices with the same name in the platform,
      run tests on all of them.
    * ``--include-pure-parallel-devices``: include pure parallel devices in the tests
      (that is, those not supporting synchronization within a block/work group).
    """
    api_shortcuts = [api_id.shortcut for api_id in all_api_ids()]
    parser.addoption(
        "--api",
        action="store",
        help="GPGPU API: " + "/".join(api_shortcuts) + " (or all available if not given)",
        default=None,
        choices=api_shortcuts,
    )

    parser.addoption(
        "--platform-include-mask",
        action="append",
        help="Run tests on matching platforms only",
        default=[],
    )
    parser.addoption(
        "--platform-exclude-mask",
        action="append",
        help="Run tests on matching platforms only",
        default=[],
    )

    parser.addoption(
        "--device-include-mask",
        action="append",
        help="Run tests on matching devices only",
        default=[],
    )
    parser.addoption(
        "--device-exclude-mask",
        action="append",
        help="Run tests on matching devices only",
        default=[],
    )

    parser.addoption(
        "--include-duplicate-devices",
        action="store_true",
        help="Run tests on all available devices and not only on uniquely named ones",
        default=False,
    )

    parser.addoption(
        "--include-pure-parallel-devices",
        action="store_true",
        help="Include pure parallel devices (not supporting synchronization within a work group)",
        default=False,
    )


@lru_cache
def get_apis(config: pytest.Config) -> list[API]:
    """Returns the list of APIs filtered by the test configuration."""
    return API.all_by_shortcut(config.option.api)


_T = TypeVar("_T")


def _concatenate(lists: Iterable[list[_T]]) -> list[_T]:
    return reduce(lambda x, y: x + y, lists, [])


@lru_cache
def get_platforms(config: pytest.Config) -> list[Platform]:
    """
    Returns the list of platforms filtered by the test configuration
    (concatenated for all filtered APIs).
    """
    apis = get_apis(config)
    return _concatenate(
        Platform.all_filtered(
            api,
            PlatformFilter(
                include_masks=config.option.platform_include_mask,
                exclude_masks=config.option.platform_exclude_mask,
            ),
        )
        for api in apis
    )


@lru_cache
def _get_device_sets(
    config: pytest.Config, unique_devices_only_override: bool | None = None
) -> list[list[Device]]:
    if unique_devices_only_override is not None:
        unique_devices_only = unique_devices_only_override
    else:
        unique_devices_only = not config.option.include_duplicate_devices

    platforms = get_platforms(config)
    return [
        Device.all_filtered(
            platform,
            DeviceFilter(
                include_masks=config.option.device_include_mask,
                exclude_masks=config.option.device_exclude_mask,
                unique_only=unique_devices_only,
                exclude_pure_parallel=not config.option.include_pure_parallel_devices,
            ),
        )
        for platform in platforms
    ]


@lru_cache
def get_devices(config: pytest.Config) -> list[Device]:
    """
    Returns the list of devices filtered by the test configuration
    (concatenated for all filtered platforms and APIs).
    """
    return _concatenate(_get_device_sets(config))


@lru_cache
def get_multi_device_sets(config: pytest.Config) -> list[list[Device]]:
    """
    Returns a list where each element is a list with two or more devices
    belonging to the same API and platform, where APIs, platforms, and devices
    are filtered by the test configuration.
    """
    device_sets = _get_device_sets(config, unique_devices_only_override=False)
    return [device_set for device_set in device_sets if len(device_set) > 1]


@pytest.fixture()
def api(request: pytest.FixtureRequest) -> API:
    """Yields the elements of the return value of :py:func:`~pytest_grunnur.get_apis`."""
    # Set in `pytest_generate_tests()`
    return cast(API, request.param)


@pytest.fixture()
def platform(request: pytest.FixtureRequest) -> Platform:
    """Yields the elements of the return value of :py:func:`~pytest_grunnur.get_platforms`."""
    # Set in `pytest_generate_tests()`
    return cast(Platform, request.param)


@pytest.fixture()
def device(request: pytest.FixtureRequest) -> Device:
    """Yields the elements of the return value of :py:func:`~pytest_grunnur.get_devices`."""
    # Set in `pytest_generate_tests()`
    return cast(Device, request.param)


@pytest.fixture()
def context(device: Device) -> Context:
    """
    A single-device context for each device yielded by
    :py:func:`~pytest_grunnur.plugin.device`.
    """
    return Context.from_devices([device])


@pytest.fixture()
def some_device(request: pytest.FixtureRequest) -> Device:
    """Yields one element of the return value of :py:func:`~pytest_grunnur.get_devices`."""
    # Set in `pytest_generate_tests()`
    return cast(Device, request.param)


@pytest.fixture()
def some_context(some_device: Device) -> Context:
    """
    A single-device context initialized with the return value of
    :py:func:`~pytest_grunnur.plugin.some_device`.
    """
    return Context.from_devices([some_device])


@pytest.fixture()
def multi_device_set(request: pytest.FixtureRequest) -> list[Device]:
    """
    Yields the elements of the return value of
    :py:func:`~pytest_grunnur.get_multi_device_sets`.
    """
    # Set in `pytest_generate_tests()`
    return cast(list[Device], request.param)


@pytest.fixture()
def multi_device_context(multi_device_set: list[Device]) -> Context:
    """
    A multi-device context for each device set yielded by
    :py:func:`~pytest_grunnur.plugin.multi_device_set`.
    """
    return Context.from_devices(multi_device_set)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """
    Seeds the parameters for the fixtures provided by this plugin
    (see the fixture list for details).
    """
    apis = get_apis(metafunc.config)
    platforms = get_platforms(metafunc.config)
    devices = get_devices(metafunc.config)

    fixtures: list[tuple[str, list[Any]]] = [
        ("api", apis),
        ("platform", platforms),
        ("device", devices),
    ]

    for name, vals in fixtures:
        if name in metafunc.fixturenames:
            metafunc.parametrize(
                name,
                vals,
                ids=["no_" + name] if len(vals) == 0 else lambda obj: cast(str, obj.shortcut),
                indirect=True,
            )

    if "some_device" in metafunc.fixturenames:
        metafunc.parametrize(
            "some_device",
            devices if len(devices) == 0 else [devices[0]],
            ids=["no_device"] if len(devices) == 0 else lambda device: cast(str, device.shortcut),
            indirect=True,
        )

    if "multi_device_set" in metafunc.fixturenames:
        device_sets = get_multi_device_sets(metafunc.config)
        ids = ["+".join(device.shortcut for device in device_set) for device_set in device_sets]
        metafunc.parametrize(
            "multi_device_set",
            device_sets,
            ids=["no_multi_device"] if len(device_sets) == 0 else ids,
            indirect=True,
        )


def pytest_report_header(config: pytest.Config) -> None:
    """
    Adds a header to the test report, listing all the GPGPU devices the tests are run on,
    including their short numerical IDs (appearing in the test parameters).
    """
    devices = get_devices(config)

    if len(devices) == 0:
        print("No GPGPU devices available")  # noqa: T201
    else:
        print("Running tests on:")  # noqa: T201
        for device in sorted(devices, key=lambda device: str(device)):
            platform = device.platform
            print(f"  {device}: {platform.name}, {device.name}")  # noqa: T201
