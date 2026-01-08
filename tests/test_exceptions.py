from foxypack.exceptions import (
    FoxyException,
    InvalidUsageException,
    ConfigurationException,
    UnsupportedOperationException,
    ImplementationContractException,
    CollectionException,
    ServiceUnavailableException,
    TimeoutException,
)


def test_all_exceptions_are_exceptions():
    exceptions = [
        FoxyException,
        InvalidUsageException,
        ConfigurationException,
        UnsupportedOperationException,
        ImplementationContractException,
        CollectionException,
        ServiceUnavailableException,
        TimeoutException,
    ]

    for exc in exceptions:
        instance = exc()
        assert isinstance(instance, Exception)


def test_collection_exception_hierarchy():
    assert issubclass(ServiceUnavailableException, CollectionException)
    assert issubclass(TimeoutException, CollectionException)
    assert issubclass(CollectionException, FoxyException)


def test_base_exception_catching():
    try:
        raise TimeoutException("timeout")
    except FoxyException as exc:
        assert isinstance(exc, TimeoutException)


def test_collection_exception_catching():
    try:
        raise ServiceUnavailableException("service down")
    except CollectionException as exc:
        assert isinstance(exc, ServiceUnavailableException)


def test_exception_message_preserved():
    message = "custom error message"
    exc = ConfigurationException(message)
    assert str(exc) == message
