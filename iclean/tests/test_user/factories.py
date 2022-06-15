from collections import OrderedDict
import factory
from faker import Faker
fake = Faker()

from apps.user.models import Role, User, Client, Company


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role
    role = fake.random_element(
    elements=OrderedDict([
        ("admin", 0.1),        # Generates "admin" 10% of the time
        ("client", 0.5),        # Generates "client" 50% of the time
        ("company", 0.4),        # Generates "company" 40% of the time
    ]))
 

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    email = fake.unique.ascii_email() 
    role = factory.SubFactory(RoleFactory)
    phone = fake.phone_number() 
    country = fake.country() 
    city = fake.city()
    is_staff = False
    is_active = True


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client
    user = factory.SubFactory(UserFactory)
    first_name = fake.first_name()
    last_name = fake.last_name() 
    street = fake.street_name() 
    house_number = int(fake.building_number())
    apartment = fake.building_number()


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
    user = factory.SubFactory(UserFactory)
    name = fake.company()
