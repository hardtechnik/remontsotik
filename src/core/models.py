import random

from django.contrib.auth import get_user_model
from django.db import IntegrityError, models
from django.urls import reverse


def generate_number():
    return str(random.randint(100000, 999999))


class Status(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        help_text='Название статуса заявки',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Этот текст будет отображаться клиенту при просмотре заявки',
    )
    ordering = models.PositiveSmallIntegerField(
        verbose_name='Позиция',
        default=1,
        blank=True,
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ('ordering',)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    status = models.ForeignKey(
        Status,
        verbose_name='Статус',
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Клиент',
        blank=True,
    )
    number = models.CharField(
        max_length=6,
        verbose_name='Номер заявки',
        db_index=True,
        unique=True,
    )
    phone_model = models.CharField(
        max_length=100,
        verbose_name='Модель',
        blank=True,
    )
    malfunction = models.TextField(
        verbose_name='Неисправность',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        blank=True,
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
    )
    address = models.CharField(
        verbose_name='Адрес',
        max_length=500,
        blank=True,
    )
    created = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ('-created',)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        if not self.pk:
            # default status from fixture
            self.status = Status.objects.get(pk=1)

        if not self.number:
            self.number = generate_number()
            for attempt in range(3):
                try:
                    return super().save(*args, **kwargs)
                except IntegrityError as e:
                    # last attempt is failed, raise error
                    if attempt == 2:
                        raise e
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ticket_detail', kwargs={'number': self.number})


class Image(models.Model):
    url = models.URLField(verbose_name='Ссылка')
    ticket = models.ForeignKey(
        Ticket,
        related_name='images',
        verbose_name='Изображение',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.url


class TicketComment(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    text = models.TextField(verbose_name='Текст')
    ticket = models.ForeignKey(
        Ticket,
        verbose_name='Заявка',
        on_delete=models.CASCADE,
    )
    posted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )

    def __str__(self):
        return f'#{self.ticket.number}'

    class Meta:
        verbose_name = 'Коментарий к заявке'
        verbose_name_plural = 'Коментарии к заявке'
        ordering = ('posted_at',)
