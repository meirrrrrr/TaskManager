from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

TASK_STATUS = (
    ('planning', 'PL'),
    ('active', 'AC'),
    ('control', 'CL'),
    ('complete', 'CE')
)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performers')
    observers = models.ManyToManyField(User)
    status = models.CharField(
        max_length=8,
        choices=TASK_STATUS
    )
    started_at = models.DateField(auto_now=True)
    planning_completed_at = models.DateField(null=True)
    completed_at = models.DateField(null=True)

    def __str__(self):
        return self.title


class ChangingStatus(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tasks')
    previous_status = models.CharField(max_length=255, null=True)
    next_status = models.CharField(
        max_length=8,
        choices=TASK_STATUS
    )
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField()
    users = models.ManyToManyField(User)
