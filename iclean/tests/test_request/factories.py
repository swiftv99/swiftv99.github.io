from collections import OrderedDict
import factory
from faker import Faker
fake = Faker()

from apps.request.models import RequestStatus, Request
from tests.test_service.factories import ServiceFactory
from tests.test_user.factories import ClientFactory, CompanyFactory


class RequestStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RequestStatus
    name = fake.random_element(
    elements=OrderedDict([
        ("ACTIVE", 0.4), 
        ("WAITING", 0.3),  
        ("CLOSED", 0.2), 
        ("REJECTED", 0.1),  
    ]))


class RequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Request
    name = fake.text(max_nb_chars=20)
    total_area = fake.random_int(min=10, max=80, step=1)
    created_at = fake.date_time_this_century()
    client = factory.SubFactory(ClientFactory)
    company = factory.SubFactory(CompanyFactory)
    status = factory.SubFactory(RequestStatusFactory)
    service = factory.SubFactory(ServiceFactory)
    slug = "request_slug"