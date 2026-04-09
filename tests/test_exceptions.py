import pytest

from foxypack import (
    FoxyError,
    InvalidUsageError,
    ConfigurationError,
    UnsupportedOperationError,
    ImplementationContractError,
    CollectionError,
    ServiceUnavailableError,
    TimeoutError,
    ContentBlockedError,
    ContentAccessError,
    ContentNotFoundError,
    ContentPrivateError,
    ContentRegionRestrictedError,
)


def test_foxy_error_minimal_init():
    err = FoxyError("something went wrong")

    assert err.message == "something went wrong"
    assert err.details == {}
    assert err.cause is None
    assert str(err) == "something went wrong"


def test_foxy_error_with_details_and_cause():
    cause = ValueError("bad value")
    err = FoxyError(
        "wrapped error",
        details={"field": "token", "reason": "missing"},
        cause=cause,
    )

    assert err.message == "wrapped error"
    assert err.details == {"field": "token", "reason": "missing"}
    assert err.cause is cause
    assert str(err) == "wrapped error | details={'field': 'token', 'reason': 'missing'}"


def test_foxy_error_to_dict_without_cause():
    err = FoxyError("simple error")

    assert err.to_dict() == {
        "type": "FoxyError",
        "message": "simple error",
        "details": {},
        "cause": None,
    }


def test_foxy_error_to_dict_with_cause():
    cause = RuntimeError("boom")
    err = FoxyError(
        "top level error",
        details={"step": "parse"},
        cause=cause,
    )

    data = err.to_dict()

    assert data["type"] == "FoxyError"
    assert data["message"] == "top level error"
    assert data["details"] == {"step": "parse"}
    assert data["cause"] == repr(cause)


@pytest.mark.parametrize(
    "exc_class",
    [
        InvalidUsageError,
        ConfigurationError,
        UnsupportedOperationError,
        ImplementationContractError,
        CollectionError,
        ContentBlockedError,
        ContentNotFoundError,
        ContentPrivateError,
        ContentRegionRestrictedError,
    ],
)
def test_specialized_exceptions_are_subclasses_of_foxy_error(exc_class):
    err = exc_class("test message")

    assert isinstance(err, FoxyError)
    assert err.message == "test message"
    assert str(err) == "test message"


def test_collection_exceptions_inherit_from_collection_error():
    service_err = ServiceUnavailableError()
    timeout_err = TimeoutError()

    assert isinstance(service_err, CollectionError)
    assert isinstance(timeout_err, CollectionError)
    assert isinstance(service_err, FoxyError)
    assert isinstance(timeout_err, FoxyError)


def test_service_unavailable_error_default_message():
    err = ServiceUnavailableError()

    assert err.message == "External service unavailable"
    assert str(err) == "External service unavailable"
    assert err.details == {}
    assert err.cause is None


def test_service_unavailable_error_custom_message():
    err = ServiceUnavailableError("API is down")

    assert err.message == "API is down"
    assert str(err) == "API is down"


def test_timeout_error_default_message():
    err = TimeoutError()

    assert err.message == "Operation timed out"
    assert str(err) == "Operation timed out"
    assert err.details == {}
    assert err.cause is None


def test_timeout_error_custom_message():
    err = TimeoutError("Request exceeded 10 seconds")

    assert err.message == "Request exceeded 10 seconds"
    assert str(err) == "Request exceeded 10 seconds"


def test_content_access_error_with_only_message():
    err = ContentAccessError("content unavailable")

    assert err.message == "content unavailable"
    assert err.details == {}
    assert err.content_id is None
    assert err.url is None
    assert err.platform is None
    assert err.cause is None
    assert str(err) == "content unavailable"


def test_content_access_error_with_context_fields():
    err = ContentAccessError(
        "content unavailable",
        content_id="123",
        url="https://example.com/post/123",
        platform="youtube",
    )

    assert err.message == "content unavailable"
    assert err.content_id == "123"
    assert err.url == "https://example.com/post/123"
    assert err.platform == "youtube"
    assert err.details == {
        "content_id": "123",
        "url": "https://example.com/post/123",
        "platform": "youtube",
    }
    assert str(err) == (
        "content unavailable | details={"
        "'content_id': '123', "
        "'url': 'https://example.com/post/123', "
        "'platform': 'youtube'"
        "}"
    )


def test_content_access_error_filters_out_none_fields():
    err = ContentAccessError(
        "not accessible",
        content_id="abc",
        url=None,
        platform=None,
    )

    assert err.details == {
        "content_id": "abc",
    }


def test_content_access_error_merges_extra_details():
    err = ContentAccessError(
        "not accessible",
        content_id="abc",
        platform="instagram",
        details={"reason": "login required", "status_code": 403},
    )

    assert err.details == {
        "content_id": "abc",
        "platform": "instagram",
        "reason": "login required",
        "status_code": 403,
    }


def test_content_access_error_extra_details_can_override_base_details():
    err = ContentAccessError(
        "not accessible",
        content_id="abc",
        url="https://example.com/original",
        details={
            "url": "https://example.com/override",
            "reason": "redirected",
        },
    )

    assert err.details == {
        "content_id": "abc",
        "url": "https://example.com/override",
        "reason": "redirected",
    }


def test_content_access_error_preserves_cause():
    cause = PermissionError("auth required")

    err = ContentAccessError(
        "private content",
        content_id="42",
        cause=cause,
    )

    assert err.cause is cause
    assert err.to_dict()["cause"] == repr(cause)


@pytest.mark.parametrize(
    "exc_class",
    [
        ContentNotFoundError,
        ContentPrivateError,
        ContentRegionRestrictedError,
    ],
)
def test_content_access_specializations_keep_context(exc_class):
    err = exc_class(
        "access problem",
        content_id="55",
        url="https://example.com/content/55",
        platform="tiktok",
        details={"status_code": 404},
    )

    assert isinstance(err, ContentAccessError)
    assert isinstance(err, FoxyError)
    assert err.content_id == "55"
    assert err.url == "https://example.com/content/55"
    assert err.platform == "tiktok"
    assert err.details == {
        "content_id": "55",
        "url": "https://example.com/content/55",
        "platform": "tiktok",
        "status_code": 404,
    }


def test_foxy_error_can_be_caught_as_exception():
    with pytest.raises(FoxyError) as exc_info:
        raise InvalidUsageError("wrong API call")

    assert str(exc_info.value) == "wrong API call"


def test_content_private_error_can_be_caught_as_content_access_error():
    with pytest.raises(ContentAccessError) as exc_info:
        raise ContentPrivateError(
            "login required",
            content_id="999",
            platform="instagram",
        )

    err = exc_info.value
    assert err.message == "login required"
    assert err.details == {
        "content_id": "999",
        "platform": "instagram",
    }