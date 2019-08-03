# Generated by Django 2.2.4 on 2019-08-03 23:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.URLField(verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='user',
        ),
        migrations.AddField(
            model_name='ticket',
            name='address',
            field=models.CharField(blank=True, max_length=500, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now, verbose_name='Время создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='Клиент'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='number',
            field=models.CharField(db_index=True, default='', max_length=6, unique=True, verbose_name='Номер заявки'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Новая'), (2, 'Проверена'), (3, 'В ремонте'), (4, 'Готова'), (5, 'Отменена'), (6, 'Выпонена')], db_index=True, default=1, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='malfunction',
            field=models.TextField(blank=True, default='', verbose_name='Неисправность'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='phone_model',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Модель'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='phone_number',
            field=models.CharField(max_length=20, verbose_name='Номер телефона'),
        ),
        migrations.DeleteModel(
            name='Malfunction',
        ),
        migrations.DeleteModel(
            name='Phone',
        ),
        migrations.AddField(
            model_name='image',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Ticket', verbose_name='Изображение'),
        ),
    ]
