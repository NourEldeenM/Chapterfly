# Generated by Django 5.0.6 on 2024-05-23 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0008_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='wishlist',
            field=models.ManyToManyField(blank=True, null=True, to='project_app.book'),
        ),
    ]
