# Generated by Django 5.0.6 on 2024-06-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0015_signup_cart_alter_signup_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='card_number',
            field=models.PositiveBigIntegerField(max_length=19),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='cvv',
            field=models.SmallIntegerField(max_length=3),
        ),
    ]
