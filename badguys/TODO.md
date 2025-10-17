# TODO: Django Task Management API Project

## STEP 1: Project Setup
- [x] Create virtual environment
- [x] Install required dependencies (django, djangorestframework, djangorestframework-simplejwt, psycopg2-binary, gunicorn, whitenoise, python-dotenv)
- [x] Create Django project named `task_management_api`
- [x] Create app named `tasks`
- [x] Configure INSTALLED_APPS in settings.py (add rest_framework, tasks)
- [x] Configure DATABASES in settings.py (SQLite for dev)
- [x] Run initial migrations
- [x] Create superuser

## STEP 2: Models
- [x] Create User model extending AbstractUser in tasks/models.py
- [x] Create Task model with all specified fields
- [x] Add model validations (due_date not in past, valid choices)
- [x] Run migrations for new models

## STEP 3: Serializers
- [x] Create UserSerializer in tasks/serializers.py
- [x] Create TaskSerializer with auto-assignment and validations

## STEP 4: Views and Permissions
- [x] Create UserViewSet and TaskViewSet using ModelViewSet
- [x] Implement CRUD operations
- [x] Override perform_create for TaskViewSet
- [x] Implement permissions (own tasks only, completed task restrictions)
- [x] Create custom endpoint for toggle_status

## STEP 5: Filtering and Sorting
- [x] Install django-filter
- [x] Add filtering and ordering to TaskViewSet (status, priority, due_date)

## STEP 6: Authentication
- [x] Configure JWT authentication in settings.py
- [x] Add token endpoints in urls.py

## STEP 7: URLs and Routing
- [x] Create tasks/urls.py with routers for users and tasks
- [x] Include tasks URLs in main urls.py

## STEP 8: Testing
- [x] Create tests in tasks/tests.py (task creation, ownership, status toggle, filters, auth)
- [x] Run all tests

## STEP 9: Deployment
- [x] Configure for deployment (gunicorn, whitenoise, ALLOWED_HOSTS, env vars)
- [x] Create requirements.txt
- [ ] Push to GitHub
- [ ] Deploy to Heroku (or similar)
- [ ] Verify deployed API

## STEP 10: Optional Stretch Goals
- [ ] (Skipped for now)
