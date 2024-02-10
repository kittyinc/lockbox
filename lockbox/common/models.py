from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from uuid import uuid4


class LockboxBase(models.Model):  # pragma: no cover
    lid = models.UUIDField(
        primary_key=True,
        default=uuid4
    )

    date_created = models.DateTimeField(
        verbose_name=_("date created")
    )
    date_updated = models.DateTimeField(
        verbose_name=_("date updated"),
        null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        now = timezone.now()

        if not self.date_created:
            self.date_created = now

        self.date_update = now

        super().save(*args, **kwargs)
