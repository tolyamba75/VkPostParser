from rest_framework import serializers

from .models import Task, ProcessingGroup, Recipient


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'group_id', 'status', 'frequency', 'last_run')


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ('admin_id', 'task')


class ProcessingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingGroup
        fields = ('id', 'task', 'group_id', 'status',
                  'launch_num', 'processed_post', 'last_post_id')
