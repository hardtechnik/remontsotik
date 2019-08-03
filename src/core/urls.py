from django.urls import path

from .views import CreateTicketView, sign_file

urlpatterns = [
    path('', CreateTicketView.as_view(), name='index'),
    path('sign-file/', sign_file, name='sign_file'),
]
