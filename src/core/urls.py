from django.urls import path

from .views import CreateTicketView, TicketDetailView, sign_file


urlpatterns = [
    path('', CreateTicketView.as_view(), name='create_ticket'),
    path('ticket/<number>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('sign-file/', sign_file, name='sign_file'),
]
