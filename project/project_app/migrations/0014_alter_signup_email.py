# Generated by Django 5.0.6 on 2024-05-25 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0013_alter_book_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='email',
            field=models.EmailField(max_length=40, unique=True),
        ),
    ]
