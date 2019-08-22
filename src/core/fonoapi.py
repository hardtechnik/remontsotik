from urllib.parse import urljoin

from django.conf import settings
import requests


API_ENDPOINT = 'https://fonoapi.freshpixl.com/v1/'
GET_DEVICE = urljoin(API_ENDPOINT, 'getdevice')


def get_device(device):
    result = requests.get(GET_DEVICE, {
        'device': device,
        'token': settings.FONOAPI_TOKEN,
    }).json()

    if isinstance(result, dict):
        return []
    return [item for item in result if item['DeviceName'] != device]
