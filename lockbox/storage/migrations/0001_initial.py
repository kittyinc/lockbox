# Generated by Django 4.2.10 on 2024-02-12 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import storage.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('lid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='lockbox ID')),
                ('date_created', models.DateTimeField(blank=True, help_text='date at which this object was created', verbose_name='date created')),
                ('date_updated', models.DateTimeField(blank=True, help_text='date at which this object was last updated', verbose_name='date updated')),
                ('name', models.CharField(help_text='display name of this file', max_length=255, verbose_name='name')),
                ('extension', models.CharField(blank=True, help_text='reported filesystem extension (not mime type)', max_length=128, null=True, verbose_name='extension')),
                ('file', models.FileField(help_text='actual file', upload_to=storage.models.get_upload_path, verbose_name='file')),
                ('position', models.PositiveBigIntegerField(default=0, help_text='current position of uploaded bytes', verbose_name='position')),
                ('status', models.CharField(choices=[('uploading', 'uploading'), ('completed', 'completed'), ('abandoned', 'abandoned')], default='uploading', help_text='upload status for file', max_length=9, verbose_name='status')),
                ('date_completed', models.DateTimeField(blank=True, help_text="datetime at which this file's upload was completed", null=True, verbose_name='completed on')),
                ('expires', models.BooleanField(default=False, help_text="will be scrubbed on 'date_expires'", verbose_name='expires')),
                ('delete_on_expiration', models.BooleanField(default=False, help_text='will be deleted if expired and expires is true', verbose_name='delete on expiration')),
                ('size_on_disk', models.PositiveBigIntegerField(blank=True, help_text='total size on disk for this file', null=True, verbose_name='size on disk (bytes)')),
                ('owner', models.ForeignKey(blank=True, help_text='owner of this file', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files_owned', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
            },
        ),
    ]