from django.core.mail import mail_managers, send_mail

from phonerepair.celery import app


send_mail = app.task(ignore_result=True)(send_mail)
mail_managers = app.task(ignore_result=True)(mail_managers)
