# Generated by Django 2.2.4 on 2019-08-04 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190804_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='description',
            field=models.TextField(help_text='Этот текст будет отображаться клиенту при просмотре заявки', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(help_text='Название статуса заявки', max_length=50, verbose_name='Название'),
        ),
    ]