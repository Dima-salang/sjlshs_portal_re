# Generated by Django 4.1.2 on 2023-03-20 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondSem_4thQ_11',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('READING_WRITING', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PAGBASA', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('STATS_PROB', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PHYSCI', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('EMPOWERMENT', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('ENTREP', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('SPECIALIZED', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('SPECIALIZED_2', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PE2', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('Average', models.IntegerField(blank=True, default=0, null=True)),
                ('lrn', models.CharField(max_length=15)),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondsem4thq11', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SecondSem_3rdQ_11',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('READING_WRITING', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PAGBASA', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('STATS_PROB', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PHYSCI', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('EMPOWERMENT', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('ENTREP', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('SPECIALIZED', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('SPECIALIZED_2', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PE2', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('Average', models.IntegerField(blank=True, default=0, null=True)),
                ('lrn', models.CharField(max_length=15)),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondsem3rdq11', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FirstSem_2ndQ_11',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('ORALCOMM', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('KOMUNIKASYON', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('GENMATH', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('ELS', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PERDEV', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('LITERATURE', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PR1', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('SPECIALIZED', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('SPECIALIZED_2', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PE', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('Average', models.IntegerField(blank=True, default=0, null=True)),
                ('lrn', models.CharField(max_length=15)),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='firstsem2ndq11', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FirstSem_1stQ_11',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('ORALCOMM', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('KOMUNIKASYON', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('GENMATH', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('ELS', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PERDEV', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('LITERATURE', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PR1', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('SPECIALIZED', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('SPECIALIZED_2', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('PE', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('Average', models.IntegerField(blank=True, default=0, null=True)),
                ('lrn', models.CharField(max_length=15)),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='firstsem1stq11', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
