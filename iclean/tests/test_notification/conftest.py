import pytest

from pytest_factoryboy import register
from tests.test_notification.factories import NotificationFactory


register(NotificationFactory)

@pytest.fixture
def notification_create(db, notification_factory):
    notification = notification_factory.create()
    return notification

@pytest.fixture
def notification_update(db, notification_factory):
    notification = notification_factory.build()
    return notification