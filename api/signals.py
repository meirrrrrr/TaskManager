from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from TaskManager.celery import app
from django.db.models import signals
from django.core.mail import send_mail
from .models import ChangingStatus
from .serializers import UserShortSerializer, ChangingStatusSerializer


def get_emails(instance):
    emails = []
    observers = UserShortSerializer(instance.observers, many=True).data
    for observer in observers:
        emails.append(observer['email'])
    return emails


def perform_mail(instance):
    emails = get_emails(instance.task)
    subject = 'Something changed with your task, check it out!'
    data = ChangingStatusSerializer(instance).data
    text = f'User {data["changed_by"]} changed status of your task from {data["previous_status"]} ' \
           f'to a {data["next_status"]}.\n'
    return [emails, subject, text]


@app.task
@receiver(pre_save, sender=ChangingStatus)
def changing_status_post_save(instance, **kwargs):
    mail = perform_mail(instance)
    send_mail(
        subject=mail[1],
        message=mail[2],
        recipient_list=mail[0],
        from_email='chegreyev@gmail.com',
        fail_silently=False
    )
