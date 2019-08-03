import posixpath

from django.conf import settings
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

import boto3
import botocore

from .forms import TicketForm


class IndexView(TemplateView):
    template_name = 'index.html'


class CreateTicketView(CreateView):
    form_class = TicketForm
    success_url = reverse_lazy('index')
    template_name = 'ticket_form.html'


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
    key = posixpath.join('uploads', filename)
    signed_data = s3.generate_presigned_post(
        Bucket=settings.PRIVATE_BUCKET,
        Key=key,
        ExpiresIn=60 * 60,
    )
    return JsonResponse(signed_data)
