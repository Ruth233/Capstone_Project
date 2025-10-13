from django.db import models
from django.conf import settings

# Create your models here.

class Task(models.Model):
    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3
    PRIORITY_CHOICES = (
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    )

    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('due_date', 'priority')

    def __str__(self):
        return f'{self.title} ({self.get_priority_display()})'
