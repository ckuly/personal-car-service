# Generated by Django 5.1.3 on 2024-11-28 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car_service', '0005_alter_car_car_model_id_alter_order_car_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': 'Car', 'verbose_name_plural': 'Cars'},
        ),
        migrations.AlterModelOptions(
            name='carmodel',
            options={'verbose_name': 'Car Model', 'verbose_name_plural': 'Car Models'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='orderservice',
            options={'verbose_name': 'Order Service', 'verbose_name_plural': 'Order Services'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Service', 'verbose_name_plural': 'Services'},
        ),
    ]
