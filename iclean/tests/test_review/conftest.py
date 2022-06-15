import pytest

from pytest_factoryboy import register
from tests.test_review.factories import ReviewFactory


register(ReviewFactory)

@pytest.fixture
def review_create(db, review_factory):
    review = review_factory.create()
    return review

@pytest.fixture
def review_update(db, review_factory):
    review = review_factory.build()
    return review