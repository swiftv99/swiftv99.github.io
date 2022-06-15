from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from apps.user.models import Company


class Service(models.Model):
    name = models.CharField(max_length=100)
    type_of_service = models.CharField(max_length=255)
    cost_of_service = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Service, self).save(*args, **kwargs)
