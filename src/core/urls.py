from django.urls import path

from .views import CreateTicketView, TicketDetailView, phone, sign_file


urlpatterns = [
    path('', CreateTicketView.as_view(), name='create_ticket'),
    path('ticket/<number>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('q', TicketDetailView.as_view(), name='ticket_search'),
    path('sign-file/', sign_file, name='sign_file'),
    path('phone/', phone, name='phone')
]
