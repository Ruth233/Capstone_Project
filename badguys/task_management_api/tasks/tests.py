from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task
from django.conf import settings

User = get_user_model()


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_task_creation(self):
        task = Task.objects.create(
            user_id=self.user.id,
            title='Test Task',
            description='Test Description',
            due_date=timezone.now().date() + timezone.timedelta(days=1),
            priority='High',
            status='Pending'
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.user, self.user)

    def test_due_date_validation(self):
        with self.assertRaises(Exception):
            Task.objects.create(
                user_id=self.user.id,
                title='Test Task',
                due_date=timezone.now().date() - timezone.timedelta(days=1),
            )


class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'Task Description',
            'due_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat(),
            'priority': 'Medium',
            'status': 'Pending'
        }
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().user, self.user)

    def test_toggle_status(self):
        task = Task.objects.create(
            user_id=self.user.id,
            title='Toggle Task',
            due_date=timezone.now().date() + timezone.timedelta(days=1),
        )
        response = self.client.post(f'/api/tasks/{task.id}/toggle_status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'Completed')

    def test_filter_tasks(self):
        Task.objects.create(user_id=self.user.id, title='Task 1', status='Pending', due_date=timezone.now().date() + timezone.timedelta(days=1))
        Task.objects.create(user_id=self.user.id, title='Task 2', status='Completed', due_date=timezone.now().date() + timezone.timedelta(days=2))
        response = self.client.get('/api/tasks/?status=Pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ownership_enforcement(self):
        other_user = User.objects.create_user(username='otheruser', email='other@example.com', password='otherpass')
        task = Task.objects.create(user_id=other_user.id, title='Other Task', due_date=timezone.now().date() + timezone.timedelta(days=1))
        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
