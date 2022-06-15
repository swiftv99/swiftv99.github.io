from django.db import models
from django.utils.text import slugify

from apps.request.models import Request
from apps.user.models import User, Company


class Notification(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='notifications')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notifications')
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Notification, self).save(*args, **kwargs)