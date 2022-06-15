from tests.test_user.factories import CompanyFactory
from tests.test_request.factories import RequestFactory
from apps.notification.models import Notification
from collections import OrderedDict
import factory
from faker import Faker
fake = Faker()


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    name = fake.text(max_nb_chars=20)
    details = fake.text(max_nb_chars=100)
    viewed_by_company = fake.random_element(
        elements=OrderedDict([
            (True, 0.5),
            (False, 0.5),
        ]))
    created_at = fake.date_time_this_century()
    request = factory.SubFactory(RequestFactory)
    company = factory.SubFactory(CompanyFactory)
    slug = "notification_slug"
