import posixpath
import uuid
from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import mail_managers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from .models import Ticket
from .forms import TicketForm
from .s3 import client as s3_client


class CreateTicketView(CreateView):
    form_class = TicketForm
    template_name = 'ticket_form.html'

    def form_valid(self, form):
        ticket = form.save()
        for url in self.request.POST.getlist('images'):
            ticket.images.create(url=url)
        admin_link = reverse('admin:core_ticket_change', args=(ticket.pk,))
        admin_link = urljoin('https://'+settings.DOMAIN, admin_link)
        mail_managers(
            'Новая заявка',
            message=f'Поступила новая заявка: {admin_link}',
            html_message=f'Поступила новая заявка: '
                    f'<a href="{admin_link}">№{ticket.number}</a>',
            fail_silently=True,
        )
        return redirect(ticket.get_absolute_url())


def ticket_detail_view(request, number):
    ticket = get_object_or_404(
        Ticket.objects.select_related('status'),
        number=number,
    )
    context = {'ticket': ticket}
    return render(request, 'ticket.html', context=context)


@require_POST
def sign_file(request):
    filename = request.POST['filename']
    s3 = s3_client()
    filename = f'{str(uuid.uuid4())[:6]}-{filename}'
    key = posixpath.join('uploads', filename)
    signed_data = s3.generate_presigned_post(
        Bucket=settings.PRIVATE_BUCKET,
        Key=key,
        ExpiresIn=60 * 60,
    )
    return JsonResponse(signed_data)
