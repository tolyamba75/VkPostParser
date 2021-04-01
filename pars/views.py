from rest_framework import viewsets

from .models import Task, ProcessingGroup, Recipient
from .permissions import APISigningPermission, TaskPermission, IsAdminPermission
from .serializers import TaskSerializer, ProcessingGroupSerializer, RecipientSerializer


class RecipientViewSet(viewsets.ModelViewSet):
    serializer_class = RecipientSerializer
    permission_classes = [APISigningPermission, IsAdminPermission]
    queryset = Recipient.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        if getattr(self, "swagger_fake_view", False):
            return Recipient.objects.none()
        group_id = self.request.query_params['vk_group_id']
        task_id = Task.objects.filter(group_id=group_id)[0].id
        return self.queryset.filter(task_id=task_id)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [APISigningPermission, TaskPermission, IsAdminPermission]
    queryset = Task.objects.all()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Task.objects.none()
        group_id = self.request.query_params['vk_group_id']
        return self.queryset.filter(group_id=group_id)


class ProcessingGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessingGroupSerializer
    permission_classes = [APISigningPermission, IsAdminPermission]
    queryset = ProcessingGroup.objects.all()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Recipient.objects.none()
        group_id = self.request.query_params['vk_group_id']
        task_id = Task.objects.filter(group_id=group_id)[0].id
        return self.queryset.filter(task_id=task_id)
