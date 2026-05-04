import pytest 
from assignments.models import Assignment 
from datetime import datetime,timezone,timedelta
@pytest.fixture
def assignment(db,course):
    return Assignment.objects.create(
            course=course,
            title="this is test",
            description="this is test description",
            deadline=datetime.now(timezone.utc)+timedelta(days=2))