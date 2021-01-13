from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, ChangingStatus, Reminder
from .serializers import TaskSerializer, ChangingStatusSerializer, ReminderSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TaskViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(performer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(performer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangingStatusViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangingStatusSerializer

    def get_queryset(self):
        return ChangingStatus.objects.filter(task__performer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        # Task data
        obj = Task.objects.get(id=int(request.data['task']))
        task_serializer = TaskSerializer(obj)
        data = task_serializer.data
        if serializer.is_valid():
            serializer.save(previous_status=data['status'], changed_by=request.user)

            task_serializer.update(obj, {'status' : request.data['next_status']})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReminderViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReminderSerializer
    queryset = Reminder.objects.all()
