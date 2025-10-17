from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Task
from .sarializers import TaskSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin
from .filters import TaskFilter

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_queryset(self):
        # non-admins only see themselves
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority']
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # If completed, prevent editing except allowed transition to pending
        if instance.status == Task.STATUS_COMPLETED:
            # allow revert only if request asks to set status to pending
            new_status = request.data.get('status', None)
            if new_status != Task.STATUS_PENDING:
                return Response(
                    {"detail": "Completed tasks cannot be edited unless you set status to 'pending' (revert)."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # else allow revert: clear completed_at in partial update handler
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # only owner permitted by permission class; optionally prevent deleting completed tasks?
        instance.delete()

    @action(detail=True, methods=['post'])
    def mark(self, request, pk=None):
        """
        POST /api/tasks/{id}/mark/  with JSON {"completed": true} or {"completed": false}
        """
        task = self.get_object()
        completed_flag = request.data.get('completed', None)
        if completed_flag is None:
            return Response({"detail": "Provide 'completed': true/false."}, status=status.HTTP_400_BAD_REQUEST)

        if completed_flag in [True, 'true', 'True', '1', 1]:
            task.status = Task.STATUS_COMPLETED
            task.completed_at = timezone.now()
            task.save()
            return Response(self.get_serializer(task).data)
        else:
            # revert to pending
            task.status = Task.STATUS_PENDING
            task.completed_at = None
            task.save()
            return Response(self.get_serializer(task).data)
