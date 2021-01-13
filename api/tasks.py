from datetime import datetime
from django.core.mail import send_mail
from TaskManager.celery import app
from .models import Task
from .serializers import TaskSerializer, UserShortSerializer


@app.task
def expire_notify():
    expired_tasks = Task.objects.filter(planning_completed_at__gte=datetime.today()).filter(completed_at=None)
    expired_tasks_ser = TaskSerializer(expired_tasks, many=True).data
    for expired_task in expired_tasks_ser:
        user = UserShortSerializer(expired_task.performer).data
        send_mail(
            subject='Task\'s duration time expired',
            message=f'Dear, {user["username"]}, please check you\'r task {expired_task["title"]}, it\'s expired',
            recipient_list=user['email'],
            from_email='chegreyev@gmail.com',
            fail_silently=False
        )
