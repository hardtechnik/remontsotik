from django.conf import settings
from django.db import models


class Phone(models.Model):
    name = models.CharField(verbose_name='Название', max_length=500)

    class Meta:
        verbose_name = 'Модель телефона'
        verbose_name_plural = 'Модели телефона'


class Malfunction(models.Model):
    name = models.CharField(verbose_name='Название', max_length=500)

    class Meta:
        verbose_name = 'Тип неисправности'
        verbose_name_plural = 'Типы неисправностей'


class Ticket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
    )
    phone_model = models.ForeignKey(
        Phone,
        verbose_name='Модель',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    malfunction = models.ForeignKey(
        Malfunction,
        verbose_name='Неисправность',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
