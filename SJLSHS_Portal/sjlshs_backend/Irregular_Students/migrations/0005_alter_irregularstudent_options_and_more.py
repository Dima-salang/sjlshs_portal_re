# Generated by Django 4.1.2 on 2023-04-21 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Irregular_Students', '0004_irregularstudent_student'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='irregularstudent',
            options={'verbose_name': 'Irregular Student', 'verbose_name_plural': 'Irregular Students'},
        ),
        migrations.AlterModelOptions(
            name='subjectgrade',
            options={'verbose_name': 'Irregular Subject Grade', 'verbose_name_plural': 'Irregular Subject Grades'},
        ),
    ]
