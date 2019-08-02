from django.urls import path, include, reverse_lazy
from django_registration.backends.one_step.views import RegistrationView

from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path(
        'accounts/register/',
        RegistrationView.as_view(success_url=reverse_lazy('index')),
        name='django_registration_register',
    ),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
