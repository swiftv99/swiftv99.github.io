import random
import factory
from faker import Faker
fake = Faker()

from apps.service.models import Service
from tests.test_user.factories import CompanyFactory


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service
    name = fake.text(max_nb_chars=20)
    type_of_service = fake.text(max_nb_chars=40)
    cost_of_service = fake.random_int(min=4, max=20, step=1)
    cost_of_service = round(random.uniform(4.00, 20.00), 2)
    created_at = fake.date_time_this_century()
    company = factory.SubFactory(CompanyFactory)
    slug = "service_slug"