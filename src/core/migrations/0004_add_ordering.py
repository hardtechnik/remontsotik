# Generated by Django 2.2.4 on 2019-08-09 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_added_status_ordering'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ('ordering',), 'verbose_name': 'Статус', 'verbose_name_plural': 'Статусы'},
        ),
    ]