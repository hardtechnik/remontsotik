from django.conf import settings


def security_headers(get_response):
    def middleware(request):
        response = get_response(request)
        response['Strict-Transport-Security'] = \
            'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = \
            f'default-src ' \
            f'{settings.S3_ENDPOINT} ' \
            f'https://mc.yandex.ru ' \
            f'https://mc.yandex.md ' \
            f'https://www.google.com ' \
            f'https://www.gstatic.com ' \
            f'https://vk.com ' \
            f'\'self\' \'unsafe-inline\' data:'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Referrer-Policy'] = 'no-referrer-when-downgrade'
        response['Feature-Policy'] = 'vibrate \'none\''
        return response
    return middleware
