# Generated by Django 4.2.6 on 2023-10-27 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='shopapp.product'),
        ),
    ]
