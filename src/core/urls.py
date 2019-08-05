from django.urls import path

from .views import CreateTicketView, sign_file, ticket_detail_view


urlpatterns = [
    path('', CreateTicketView.as_view(), name='create_ticket'),
    path('ticket/<number>/', ticket_detail_view, name='ticket_detail'),
    path('sign-file/', sign_file, name='sign_file'),
]
