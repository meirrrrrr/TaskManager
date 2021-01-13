from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Task, ChangingStatus, Reminder


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserShortSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskSerializer(ModelSerializer):
    performer = StringRelatedField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'performer', 'observers',
                  'status', 'started_at', 'planning_completed_at', 'completed_at'
                  ]
        read_only_fields = ['performer', 'started_at', 'completed_at']

    def to_representation(self, instance):
        representation = super(TaskSerializer, self).to_representation(instance)
        representation['observers'] = UserShortSerializer(many=True, instance=instance.observers).data
        return representation


class ChangingStatusSerializer(ModelSerializer):
    changed_by = StringRelatedField()

    class Meta:
        model = ChangingStatus
        fields = ['id', 'previous_status', 'next_status', 'task', 'changed_by']
        read_only_fields = ['previous_status', 'changed_by']

    def to_representation(self, instance):
        representation = super(ChangingStatusSerializer, self).to_representation(instance)
        representation['status'] = TaskSerializer(instance=instance.task).data
        return representation


class ReminderSerializer(ModelSerializer):
    users = StringRelatedField(many=True)

    class Meta:
        model = Reminder
        fields = ['id', 'task', 'text', 'users']
