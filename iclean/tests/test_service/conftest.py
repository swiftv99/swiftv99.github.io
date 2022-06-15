import pytest

from pytest_factoryboy import register
from tests.test_service.factories import ServiceFactory


register(ServiceFactory)

@pytest.fixture
def service_create(db, service_factory):
    service = service_factory.create()
    return service

@pytest.fixture
def service_update(db, service_factory):
    service = service_factory.build()
    return service