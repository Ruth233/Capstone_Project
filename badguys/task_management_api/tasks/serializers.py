from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task
from django.utils import timezone
from django.conf import settings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'due_date', 'priority', 'status', 'completed_at', 'created_at', 'updated_at']
        read_only_fields = ['completed_at', 'created_at', 'updated_at']

    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate(self, data):
        instance = self.instance
        if instance and instance.status == 'Completed' and data.get('status') != 'Pending':
            raise serializers.ValidationError("Cannot update a completed task unless reverting to pending.")
        return data

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.status == 'Completed' and validated_data.get('status') != 'Pending':
            raise serializers.ValidationError("Cannot update a completed task unless reverting to pending.")
        return super().update(instance, validated_data)
