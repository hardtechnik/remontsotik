import posixpath
import uuid

from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, CreateView

import boto3
import botocore

from .models import Ticket
from .forms import TicketForm


class IndexView(TemplateView):
    template_name = 'index.html'


class CreateTicketView(CreateView):
    form_class = TicketForm
    template_name = 'ticket_form.html'

    def form_valid(self, form):
        ticket = form.save()
        for url in self.request.POST.getlist('images'):
            ticket.images.create(url=url)
        return redirect(ticket.get_absolute_url())


def ticket_detail_view(request, number):
    ticket = get_object_or_404(
        Ticket.objects.select_related('status'),
        number=number,
    )
    context = {'ticket': ticket}
    return render(request, 'ticket_created.html', context=context)


def sign_file(request):
    if not request.method == 'POST':
        raise Http404()
    filename = request.POST['filename']
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='ru-central1',
        endpoint_url='https://storage.yandexcloud.net',
        config=botocore.client.Config(signature_version='s3v4'),
    )
    filename = f'{str(uuid.uuid4())[:6]}-{filename}'
    key = posixpath.join('uploads', filename)
    signed_data = s3.generate_presigned_post(
        Bucket=settings.PRIVATE_BUCKET,
        Key=key,
        ExpiresIn=60 * 60,
    )
    return JsonResponse(signed_data)
