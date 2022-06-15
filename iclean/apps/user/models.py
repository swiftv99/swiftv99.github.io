from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'ADMIN'),
        ('client', 'CLIENT'),
        ('company', 'COMPANY'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True)

    class Meta:
        ordering = ['role']

    def __str__(self):
        return self.role.capitalize()


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, related_name='users')
    phone = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['email']

    def str(self):
        return self.email


class Client(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name='clients')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.PositiveSmallIntegerField()
    apartment = models.CharField(max_length=255)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
  
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Company(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name='companys')
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['user']
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name