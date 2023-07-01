# Generated by Django 3.2.14 on 2022-08-21 02:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WebauthnDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The human-readable name of this device.', max_length=64)),
                ('confirmed', models.BooleanField(default=True, help_text='Is this device ready for use?')),
                (
                    'throttling_failure_timestamp',
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        help_text='A timestamp of the last failed verification attempt.'
                                  ' Null if last attempt succeeded.',
                        null=True,
                    ),
                ),
                (
                    'throttling_failure_count',
                    models.PositiveIntegerField(
                        default=0,
                        help_text='Number of successive failed attempts.',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_used_at', models.DateTimeField(null=True)),
                ('public_key', models.TextField(unique=True)),
                ('key_handle', models.TextField()),
                ('sign_count', models.IntegerField()),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='webauthn_keys',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
