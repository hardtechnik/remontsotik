from django.urls import reverse


def common(request):
    return {
        'show_log_in': request.path not in (
            reverse(view) for view in (
                'login',
                'django_registration_register',
            )
        )
    }
