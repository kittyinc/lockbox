import hashlib
from pathlib import Path

from common.constants import CONFIG_KEYS, UPLOAD_STATUS_TYPES
from common.models import LockboxBase
from common.utils import get_config, normalize_string
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_upload_path(instance, filename):
    filename = normalize_string(filename) + ".part"
    file_subdir = settings.MEDIA_ROOT / str(instance.lid)

    if not Path.exists(file_subdir):
        Path.mkdir(file_subdir)

    return Path(str(instance.lid)) / Path(filename)


class File(LockboxBase):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name = _("name"),
        help_text=_("display name of this file"),
    )

    extension = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("extension"),
        help_text=_("reported filesystem extension (not mime type)"),
    )

    file = models.FileField(
        upload_to=get_upload_path,
        null=False,
        blank=False,
        verbose_name=_("file"),
        help_text=_("actual file"),
    )

    position = models.PositiveBigIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name=_("position"),
        help_text=_("current position of uploaded bytes"),
    )

    UPLOAD_CHOICES = (
        (UPLOAD_STATUS_TYPES.UPLOADING, _(UPLOAD_STATUS_TYPES.UPLOADING)),
        (UPLOAD_STATUS_TYPES.COMPLETED, _(UPLOAD_STATUS_TYPES.COMPLETED)),
        (UPLOAD_STATUS_TYPES.ABANDONED, _(UPLOAD_STATUS_TYPES.ABANDONED)),
    )

    status = models.CharField(
        max_length=9,
        choices=UPLOAD_CHOICES,
        default=UPLOAD_STATUS_TYPES.UPLOADING,
        blank=False,
        null=False,
        verbose_name=_("status"),
        help_text=_("upload status for file"),
    )

    date_completed = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("completed on"),
        help_text=_("datetime at which this file's upload was completed"),
    )

    owner = models.ForeignKey(
        "user.LockboxUser",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="files_owned",
        verbose_name=_("owner"),
        help_text=_("owner of this file"),
    )

    expires = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name = _("expires"),
        help_text=_("will be scrubbed on 'date_expires'"),
    )

    delete_on_expiration = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_("delete on expiration"),
        help_text=_("will be deleted if expired and expires is true"),
    )

    size_on_disk = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name=_("size on disk (bytes)"),
        help_text=_("total size on disk for this file"),
    )

    readonly_fields = [
        "extension",
        "position",
        "status",
        "date_completed",
        "size_on_disk",
        *LockboxBase.readonly_fields,
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("file")
        verbose_name_plural = _("files")

    @property
    def md5(self):
        if getattr(self, "_md5", None) is None:
            md5 = hashlib.md5()  # noqa:S324 this is needed due to how chunked files work.
            for chunk in self.file.chunks():
                md5.update(chunk)
            self._md5 = md5.hexdigest()
        return self._md5

    @property
    def date_expires(self):
        return self.date_created + get_config(CONFIG_KEYS["EXPIRATION_DELTA_MINUTES"])

    @property
    def abandoned(self):
        return self.date_created + get_config(CONFIG_KEYS["ABANDONED_DELTA_MINUTES"])

    @property
    def expired(self):
        return self.date_expires <= timezone.now()

    def delete(self, *args, delete_file=True, **kwargs):
        if self.file:
            storage, path = self.file.storage, self.file.path
        super().delete(*args, **kwargs)
        if self.file and delete_file:
            storage.delete(path)

    def get_file_handler_bytes(self):
        self.file.close()
        self.file.open(mode="rb")
        return UploadedFile(file=self.file, name=self.filename, size=self.offset)

    def append_chunk(self, chunk, chunk_size=None, save=None):
        # file handler might be open for some bizzare reason
        self.file.close()

        with Path.open(self.file.path, mode="ab") as fh:
            fh.write(
                chunk.read(),
            )

        if chunk_size is not None:
            # file is chunked
            self.postition += chunk_size
        elif hasattr(chunk, "size"):
            self.postition += chunk.size
        else:
            # file is one shot (small file)
            self.postition = self.file.size
        self._md5 = None
        if save:
            self.save()
        self.file.close()


# class FileShare(LockboxBase):
#     file = models.ForeignKey(
#         "storage.File",
#         null=False,
#         blank=False,
#         on_delete=models.CASCADE,
#         related_name="shares",
#     )

#     def __str__(self):
#         return self.file.name

#     class Meta:
#         verbose_name = _("share")
#         verbose_name_plural = _("shares")
