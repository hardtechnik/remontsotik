import random
from django.db import models, IntegrityError


def generate_number():
    return str(random.randint(100000, 999999))


class Ticket(models.Model):
    STATUS_CREATED = 1
    STATUS_APPROVED = 2
    STATUS_IN_PROGRESS = 3
    STATUS_READY = 4
    STATUS_CANCELED = 5
    STATUS_DONE = 6

    STATUSES = (
        (STATUS_CREATED, 'Новая'),
        (STATUS_APPROVED, 'Проверена'),
        (STATUS_IN_PROGRESS, 'В ремонте'),
        (STATUS_READY, 'Готова'),
        (STATUS_CANCELED, 'Отменена'),
        (STATUS_DONE, 'Выпонена'),
    )
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=STATUSES,
        default=STATUS_CREATED,
        db_index=True,
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Клиент',
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
    ),
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

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        if self.number:
            return super().save(*args, **kwargs)

        self.number = generate_number()
        for attempt in range(3):
            try:
                return super().save(*args, **kwargs)
            except IntegrityError as e:
                # last attempt is failed, raise error
                if attempt == 2:
                    raise e


class Image(models.Model):
    file = models.URLField(verbose_name='Ссылка')
    ticket = models.ForeignKey(
        Ticket,
        verbose_name='Изображение',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
