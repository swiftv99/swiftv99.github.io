from celery import shared_task
from apps.user.models import User, Client, Company


@shared_task
def say_count():
    user_count = User.objects.all().count()
    client_count = Client.objects.all().count()
    company_count = Company.objects.all().count()
    return f"Users: {user_count}, Clients: {client_count}, Companies: {company_count}"
