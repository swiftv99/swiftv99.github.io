from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

from apps.service.models import Service
from apps.user.models import Client


class Review(models.Model):
    comment = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='reviews')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"{self.client} - ({self.created_at})"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.comment)
        super(Review, self).save(*args, **kwargs)