import posixpath
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView

from .forms import TicketForm
from .models import Ticket
from .s3 import client as s3_client


class CreateTicketView(CreateView):
    form_class = TicketForm
    template_name = 'ticket_form.html'

    def form_valid(self, form):
        ticket = form.save()
        for url in self.request.POST.getlist('images'):
            ticket.images.create(url=url)
        return redirect(ticket.get_absolute_url())


class TicketDetailView(DetailView):
    queryset = Ticket.objects.select_related('status')
    template_name = 'ticket.html'
    context_object_name = 'ticket'
    slug_url_kwarg = 'number'
    slug_field = 'number'

    def get_object(self, queryset=None):
        if self.kwargs:
            return super().get_object(queryset)
        number = self.request.GET.get('number')
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, number=number)


@require_POST
def sign_file(request):
    filename = request.POST['filename']
    s3 = s3_client()
    filename = f'{str(uuid.uuid4())[:6]}-{filename}'
    key = posixpath.join('uploads', filename)
    signed_data = s3.generate_presigned_post(
        Bucket=settings.PRIVATE_BUCKET,
        Key=key,
        ExpiresIn=60*60,
    )
    return JsonResponse(signed_data)
