from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField
from group.models import Group


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=20, blank=False)
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, null=True
    )
