from datetime import timedelta
from pathlib import Path

from common.constants import CONFIG_KEYS, UPLOAD_STATUS_TYPES
from common.models import LockboxBase
from common.utils import get_config, get_max_size_chunk_bytes, normalize_string
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_upload_path_chunk(instance, filename):
    file_subdir = settings.MEDIA_ROOT / str(instance.file.lid)

    if not Path.exists(file_subdir):
        Path.mkdir(file_subdir)

    filename = f"{FileChunk.last_chunk_id(instance.file)}.chunk"
    return Path(str(instance.lid)) / Path(filename)

class File(LockboxBase):
    filename = models.CharField(
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
        null=True,
        blank=True,
        verbose_name=_("file"),
        help_text=_("actual file"),
    )

    UPLOAD_CHOICES = (
        (UPLOAD_STATUS_TYPES.UPLOADING, _(UPLOAD_STATUS_TYPES.UPLOADING)),
        (UPLOAD_STATUS_TYPES.COMPLETED, _(UPLOAD_STATUS_TYPES.COMPLETED)),
        (UPLOAD_STATUS_TYPES.PROCESSING, _(UPLOAD_STATUS_TYPES.PROCESSING)),
        (UPLOAD_STATUS_TYPES.ABANDONED, _(UPLOAD_STATUS_TYPES.ABANDONED)),
    )

    status = models.CharField(
        max_length=10,
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

    max_size_chunk_bytes = models.PositiveBigIntegerField(
        null=False,
        blank=False,
        default=get_max_size_chunk_bytes,
        verbose_name=_("maximum size of chunks (bytes)"),
        help_text=_("max size of each individual chunk for this file"),
    )

    readonly_fields = [
        "extension",
        "status",
        "date_completed",
        "size_on_disk",
        "file",
        "max_size_chunk_bytes",
        *LockboxBase.readonly_fields,
    ]

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = _("file")
        verbose_name_plural = _("files")

    @property
    def checksum(self):
        return 0

    @property
    def date_expires(self):
        return self.date_created + timedelta(minutes=get_config("EXPIRATION_DELTA_MINUTES").value)

    @property
    def abandoned(self):
        return self.date_created + timedelta(minutes=get_config("ABANDONED_DELTA_MINUTES").value)

    @property
    def expired(self):
        return self.date_expires <= timezone.now()

    def delete(self, *args, delete_file=True, **kwargs):
        if self.file:
            storage, path = self.file.storage, self.file.path
        super().delete(*args, **kwargs)
        if self.file and delete_file:
            storage.delete(path)

        # clean up chunks in case they have not been cleaned up by task.
        self.chunks.all().delete()

    def get_file_handler_bytes(self):
        self.file.close()
        self.file.open(mode="rb")
        return UploadedFile(file=self.file, name=self.filename, size=self.offset)


class FileChunk(LockboxBase):
    file = models.ForeignKey(
        "storage.File",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="chunks",
    )

    chunk = models.FileField(
        upload_to=get_upload_path_chunk,
        null=False,
        blank=False,
        verbose_name=_("file"),
        help_text=_("actual file"),
    )

    chunk_id = models.BigIntegerField(
        null=False,
        blank=False,
        verbose_name=_("chunk id"),
        help_text=_("part of chunk"),
    )

    size = models.BigIntegerField(
        null=False,
        blank=False,
        verbose_name=("size"),
        help_text=_("size for this chunk"),
    )

    start = models.BigIntegerField(
        null=False,
        blank=False,
        verbose_name=("start"),
        help_text=_("start for this chunk"),
    )

    end = models.BigIntegerField(
        null=False,
        blank=False,
        verbose_name=("end"),
        help_text=_("end for this chunk"),
    )

    owner = models.ForeignKey(
        "user.LockboxUser",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="chunks_owned",
        verbose_name=_("owner"),
        help_text=_("owner of this file chunk"),
    )

    readonly_fields = [
        "file",
        "chunk_id",
        "start",
        "end",
        "size",
        *LockboxBase.readonly_fields,
    ]

    def __str__(self):
        return f"{self.file.filename}.{self.chunk_id}.chunk"

    class Meta:
        verbose_name = _("file chunk")
        verbose_name_plural = _("file chunks")
        unique_together = ("file", "chunk_id")

    def save(self, *args, **kwargs):
        # nasty hack lol
        self.chunk_id = int(Path(self.file.name).stem)
        return super().save(*args, **kwargs)

    def delete(self, *args, delete_file=True, **kwargs):
        if self.chunk:
            storage, path = self.chunk.storage, self.chunk.path
        super().delete(*args, **kwargs)
        if self.chunk and delete_file:
            storage.delete(path)

    @staticmethod
    def last_chunk_id(file_lid):
        last_chunk = (
            FileChunk.objects.filter(
                file__lid=file_lid,
            )
            .order_by("-chunk_id")
            .values("chunk_id")
            .first()
            .get("chunk_id")
        )

        if last_chunk:
            return last_chunk + 1
        return 1


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
