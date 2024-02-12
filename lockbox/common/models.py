from typing import Any, NamedTuple
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.constants import CONFIG_KEYS
from common.utils import cast_to_native_type


class LockboxBase(models.Model):  # pragma: no cover
    lid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        verbose_name=_("lockbox ID"),
    )

    date_created = models.DateTimeField(
        verbose_name=_("date created"),
        help_text=_("date at which this object was created"),
        null=False,
        blank=True,
    )

    date_updated = models.DateTimeField(
        verbose_name=_("date updated"),
        help_text=_("date at which this object was last updated"),
        null=False,
        blank=True,
    )

    readonly_fields = [
        "date_created",
        "date_updated",
        "lid",
    ]

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        now = timezone.now()

        if not self.date_created:
            self.date_created = now

        self.date_updated = now

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__} Object {self.lid}"


class Config(NamedTuple):
    key: str
    value: Any
    native_type: type # change to type
    description: str
    source: str
    default: Any


class Configuration(LockboxBase):

    CONFIG_KEY_CHOICES = (
        (key, value["description"]) for key, value in CONFIG_KEYS.items()
    )

    key = models.CharField(
        choices=CONFIG_KEY_CHOICES,
        max_length=50,
        null=False,
        blank=False,
        help_text=_("internal configuration key name"),
    )

    value = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
        help_text=_("actual DB config value"),
    )

    readonly_fields = LockboxBase.readonly_fields

    def save(self, *args, **kwargs):
        native_type = CONFIG_KEYS[self.key]["native_type"]
        cast_to_native_type(self.key, self.value, native_type)
        return super().save(*args, **kwargs)
