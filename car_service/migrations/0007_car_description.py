# Generated by Django 5.1.3 on 2024-12-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service', '0006_alter_car_options_alter_carmodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='description',
            field=models.TextField(default='', max_length=2000, verbose_name='Description'),
        ),
    ]