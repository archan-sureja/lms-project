import pytest 
from accounts.models import User ,EmployeeProfile , Department , Level
from rest_framework.test import APIClient

@pytest.fixture
def emp_profile(db):
    dept = Department.objects.create(name="PYTHON")
    level = Level.objects.create(level="TRAINEE")
    return EmployeeProfile.objects.create(department=dept,level=level)

@pytest.fixture
def user(db,emp_profile):
    return User.objects.create_user(
        username="testuser",
        password="password@1234",
        email="test@example.com",
        role="LEARNER",
        employee_profile=emp_profile)

@pytest.fixture
def api_client():
    return APIClient()