from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import mail_managers, send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from phonerepair.celery import app

from .models import Ticket


@app.task(ignore_result=True)
def send_status_email(ticket_id):
    ticket = Ticket.objects.exclude(email='').filter(id=ticket_id).first()
    if not ticket:
        return

    subject = f'Заявка №{ticket.number}'
    context = {'ticket': ticket, 'subject': subject}
    message = render_to_string('dist/ticket-status.html', context)
    send_mail(
        subject,
        ticket.status.description,
        'Ремонт Сотик <noreply@remontsotik.com>',
        [ticket.email],
        html_message=message,
    )


@app.task(ignore_result=True)
def send_new_ticket_created_email(ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    admin_link = reverse('admin:core_ticket_change', args=(ticket_id,))
    admin_link = urljoin('https://' + settings.DOMAIN, admin_link)
    mail_managers(
        'Новая заявка',
        message=f'Поступила новая заявка: {admin_link}',
        html_message=f'Поступила новая заявка: '
                     f'<a href="{admin_link}">№{ticket.number}</a>',
    )
