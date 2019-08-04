# Generated by Django 2.2.4 on 2019-08-04 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Клиент')),
                ('number', models.CharField(db_index=True, max_length=6, unique=True, verbose_name='Номер заявки')),
                ('phone_model', models.CharField(blank=True, max_length=100, verbose_name='Модель')),
                ('malfunction', models.TextField(blank=True, verbose_name='Неисправность')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=500, verbose_name='Адрес')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Status', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.Ticket', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]
