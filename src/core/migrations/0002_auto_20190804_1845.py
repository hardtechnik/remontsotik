# Generated by Django 2.2.4 on 2019-08-04 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Клиент'),
        ),
    ]
