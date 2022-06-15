import random
import factory
from faker import Faker
fake = Faker()

from apps.review.models import Review
from tests.test_user.factories import ClientFactory, CompanyFactory


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review
    comment = fake.text(max_nb_chars=200)
    rating = round(random.uniform(0.0, 5.0), 2)
    created_at = fake.date_time_this_century()
    client = factory.SubFactory(ClientFactory)
    company = factory.SubFactory(CompanyFactory)
    slug = "review_slug"