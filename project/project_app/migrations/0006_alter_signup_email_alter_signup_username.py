# Generated by Django 5.0.6 on 2024-05-23 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0005_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='email',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='signup',
            name='username',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]