# Generated by Django 5.0.6 on 2024-05-20 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardholder_name', models.CharField(max_length=255)),
                ('card_number', models.CharField(max_length=19)),
                ('card_type', models.CharField(choices=[('Visa', 'Visa'), ('MasterCard', 'MasterCard'), ('amex', 'amex'), ('payPal', 'payPal')], max_length=10)),
                ('expiration_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name': 'Checkout',
                'verbose_name_plural': 'Checkouts',
                'ordering': ['cardholder_name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('name', models.CharField(max_length=100, verbose_name='Book Name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Price')),
                ('descritption', models.TextField(verbose_name='Description')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Book ID')),
                ('author', models.CharField(max_length=100)),
                ('img', models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d')),
                ('available', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('available', 'available'), ('borrowed', 'borrowed'), ('sold', 'sold')], max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='project_app.category')),
            ],
        ),
    ]
