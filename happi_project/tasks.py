from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_client_email(subject, content, client_email):
    client_email = EmailMessage(
        subject,
        content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[client_email]
    )
    client_email.send()

@shared_task
def send_practitioner_email(subject, content, practitioner_email):
    practitioner_email = EmailMessage(
        subject,
        content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[practitioner_email]
    )
    practitioner_email.send()
