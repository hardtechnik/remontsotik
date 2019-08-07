FROM python:3.7.4-slim-stretch

ENV PYTHONUNBUFFERED=1

ADD ./src /src

WORKDIR /src

RUN set -x \
    && buildDeps='gcc libc-dev' \
    && apt-get update && apt-get install -y --no-install-recommends \
        $buildDeps \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uwsgi \
    && pip install --no-cache-dir -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && find /src -type d -name __pycache__ -exec rm -rf '{}' + \
    && apt-get purge -y --auto-remove $buildDeps

CMD uwsgi --socket 0.0.0.0:8000 --wsgi-file ./phonerepair/wsgi.py
