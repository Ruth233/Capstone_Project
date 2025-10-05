# Capstone_Project
# Task Management API (Django + DRF)

A Task Management REST API built with Django and Django REST Framework (DRF). Features:
- User registration & authentication (JWT)
- CRUD for tasks
- Mark tasks complete / incomplete (with completed_at timestamp)
- Filters and ordering (status, priority, due dates)
- Permissions: users only access their own tasks

---

## Quick local setup

Prereqs: Python 3.10+, git.

1. Clone & create env
```bash
git clone <your-repo-url>
cd taskmanager
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
