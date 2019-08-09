from django.db import transaction
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

from .models import Ticket
from .tasks import send_new_ticket_created_email, send_status_email


@receiver(post_init, sender=Ticket)
def set_previous_state_id(instance, **kwargs):
    instance.previous_status_id = getattr(instance, 'status_id', None) \
        if instance.id else None


@receiver(post_save, sender=Ticket, dispatch_uid="send_status_update")
def send_status_update(instance, created, **kwargs):
    def on_commit():
        if created:
            send_new_ticket_created_email.delay(instance.id)
        if instance.status_id != instance.previous_status_id:
            send_status_email.delay(instance.id)

    transaction.on_commit(on_commit)
