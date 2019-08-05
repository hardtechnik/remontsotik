from functools import lru_cache

from django.conf import settings

import boto3
import botocore


@lru_cache(maxsize=1)
def client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='ru-central1',
        endpoint_url='https://storage.yandexcloud.net',
        config=botocore.client.Config(signature_version='s3v4'),
    )


def get_presigned_url(key, expires_in=60):
    s3 = client()
    return s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': settings.PRIVATE_BUCKET,
            'Key': key,
        },
        ExpiresIn=expires_in,
    )
