import pytest

from pytest_factoryboy import register
from tests.test_user.factories import RoleFactory, UserFactory, ClientFactory, CompanyFactory


register(RoleFactory)
register(UserFactory)
register(ClientFactory)
register(CompanyFactory)

# Role model fixtures
@pytest.fixture
def role_create(db, role_factory):
    role = role_factory.create()
    return role

@pytest.fixture
def role_update(db, role_factory):
    role = role_factory.build()
    return role


# User model fixtures
@pytest.fixture
def user_create(db, user_factory):
    user = user_factory.create()
    return user

@pytest.fixture
def user_update(db, user_factory):
    user = user_factory.build()
    return user


# Client model fixtures
@pytest.fixture
def client_create(db, client_factory):
    client = client_factory.create()
    return client

@pytest.fixture
def client_update(db, client_factory):
    client = client_factory.build()
    return client


# Company model fixtures
@pytest.fixture
def company_create(db, company_factory):
    company = company_factory.create()
    return company

@pytest.fixture
def company_update(db, company_factory):
    company = company_factory.build()
    return company