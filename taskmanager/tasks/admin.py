from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'priority', 'status', 'due_date', 'completed_at')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description', 'owner__username')
