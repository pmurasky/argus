from argus import ArgusError
from argus.loader import PackNotFoundError
from argus.generator import UnknownPlatformError, AdapterConflictError


def test_pack_not_found_error_is_argus_error():
    assert issubclass(PackNotFoundError, ArgusError)


def test_unknown_platform_error_is_argus_error():
    assert issubclass(UnknownPlatformError, ArgusError)


def test_adapter_conflict_error_is_argus_error():
    assert issubclass(AdapterConflictError, ArgusError)
