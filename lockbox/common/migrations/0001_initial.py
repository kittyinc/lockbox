# Generated by Django 4.2.10 on 2024-02-13 09:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('lid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='lockbox ID')),
                ('date_created', models.DateTimeField(blank=True, help_text='date at which this object was created', verbose_name='date created')),
                ('date_updated', models.DateTimeField(blank=True, help_text='date at which this object was last updated', verbose_name='date updated')),
                ('key', models.CharField(choices=[('EXPIRATION_DELTA_MINUTES', 'Date created + this delta at which file expires'), ('ABANDONED_DELTA_MINUTES', 'Date created + this delta at which a file is marked as abandoned'), ('ABANDONED_EXPIRED_SCAN_INTERVAL', 'Scan and scrub abandoned or expired uploads'), ('MAX_UPLOAD_BYTES', 'Max bytes that can be uploaded in one go')], help_text='internal configuration key name', max_length=50)),
                ('value', models.CharField(help_text='actual DB config value', max_length=1024)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
