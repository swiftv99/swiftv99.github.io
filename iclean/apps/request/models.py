from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from apps.user.models import Client, Company
from apps.service.models import Service


class RequestStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'requeststatuses'

    def __str__(self):
        return self.name


class Request(models.Model):
    name = models.CharField(max_length=100)
    total_area = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='requests')
    status = models.ForeignKey(RequestStatus, on_delete=models.PROTECT, null=True, related_name='requests')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Request, self).save(*args, **kwargs)