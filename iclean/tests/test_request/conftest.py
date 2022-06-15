import pytest

from pytest_factoryboy import register
from tests.test_request.factories import RequestStatusFactory, RequestFactory


register(RequestStatusFactory)
register(RequestFactory)

# RequestStatus model fixtures
@pytest.fixture
def request_status_create(db, request_status_factory):
    request_status = request_status_factory.create()
    return request_status

@pytest.fixture
def request_status_update(db, request_status_factory):
    request_status = request_status_factory.build()
    return request_status

# Request model fixtures
@pytest.fixture
def request_create(db, request_factory):
    request = request_factory.create()
    return request

@pytest.fixture
def request_update(db, request_factory):
    request = request_factory.build()
    return request