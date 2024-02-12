from common.models import LockboxBase
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.managers import LockboxUserManager


class LockboxUser(AbstractUser, LockboxBase):
    alias = models.SlugField(
        verbose_name=_("name"),
        max_length=32,
        unique=True,
        null=True,
        blank=True,
        help_text=_("an alias or nickname to remember who this is"),
    )

    # Void this stuff.
    email = None
    first_name = None
    last_name = None

    objects = LockboxUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = None
    REQUIRED_FIELDS = [
        "alias",
    ]

    def __str__(self):
        if self.alias:
            return f"{self.username} ({self.alias})"
        return f"{self.username}"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
