from django.conf import settings


def security_headers(get_response):
    def middleware(request):
        response = get_response(request)
        response['Strict-Transport-Security'] = \
            'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = \
            f'default-src {settings.S3_ENDPOINT} https://mc.yandex.ru ' \
            f'\'self\' \'unsafe-inline\' data:'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Referrer-Policy'] = 'no-referrer-when-downgrade'
        response['Feature-Policy'] = 'vibrate \'none\''
        return response
    return middleware
