import pytest 
from accounts.models import User ,EmployeeProfile , Department , Level
from courses.models import Tag, Course, Topic , Enrollment
from assignments.models import Assignment 
from rest_framework.test import APIClient
from datetime import datetime,timezone,timedelta
@pytest.fixture
def emp_profile(db):
    dept = Department.objects.create(name="PYTHON")
    level = Level.objects.create(level="TRAINEE")
    return EmployeeProfile.objects.create(department=dept,level=level)

@pytest.fixture
def user(db,emp_profile):
    return User.objects.create_user(
        username="testinstructor",
        password="password@1234",
        email="instructor@example.com",
        role="INSTRUCTOR",
        employee_profile=emp_profile)

@pytest.fixture
def other_instructor(db,emp_profile):
    return User.objects.create_user(
        username="testinstructor1",
        password="password@1234",
        email="instructor@example.com",
        role="INSTRUCTOR",
        employee_profile=emp_profile)

@pytest.fixture
def learner_user(db,emp_profile):
    return User.objects.create_user(
        username="testuser",
        password="password@1234",
        email="learner@example.com",
        role="LEARNER",
        employee_profile=emp_profile)

@pytest.fixture
def other_learner_user(db,emp_profile):
    return User.objects.create_user(
        username="testuser1",
        password="password@1234",
        email="learner1@example.com",
        role="LEARNER",
        employee_profile=emp_profile)

@pytest.fixture
def tags(db):
    lst = []
    for i in range(5):
        lst = [Tag.objects.create(name=f"tag{i}")]
    return lst

@pytest.fixture
def courses_created_by_user(db,user,tags):
    for i in range(5):
        course = Course.objects.create(
                    title=f"title{i+1}",
                    description=f"some descpription for course {i+1}",
                    instructor=user
                )  
        course.tags.set(tags) 
        for j in range(5):
            Topic.objects.create(
                name=f"test topic {j+1}",
                resource_link=f"http://resources{j+1}.com",
                course=course)
    return Course.objects.all()

@pytest.fixture
def course(db,user,tags):
    course = Course.objects.create(
                    title="title_test",
                    description="some descpription for course(testing)",
                    instructor=user
                )  
    course.tags.set(tags) 
    for j in range(5):
            Topic.objects.create(
                name=f"test topic {j+1}",
                resource_link=f"http://resources{j+1}.com",
                course=course)
    return course

@pytest.fixture
def enrollments(db,learner_user,other_learner_user,course):
    Enrollment.objects.create(course=course,user=learner_user)
    Enrollment.objects.create(course=course,user=other_learner_user)
    return Enrollment.objects.all()

@pytest.fixture
def not_allowed_dept_course(db,user,learner_user):
    course = Course.objects.create(
        title="title_test",
        description="some descpription for course(testing)",
        instructor=user
    )
    for j in range(5):
            Topic.objects.create(
                name=f"test topic {j+1}",
                resource_link=f"http://resources{j+1}.com",
                course=course)
    course.allowed_depts.set([Department.objects.create(name="QA")])
    course.allowed_levels.set([learner_user.employee_profile.level])
    return course 

@pytest.fixture
def not_allowed_level_course(db,user,learner_user):
    course = Course.objects.create(
        title="title_test",
        description="some descpription for course(testing)",
        instructor=user
    )
    for j in range(5):
            Topic.objects.create(
                name=f"test topic {j+1}",
                resource_link=f"http://resources{j+1}.com",
                course=course)
    course.allowed_depts.add(learner_user.employee_profile.department)
    course.allowed_levels.set([Level.objects.create(level="JR.")])
    return course
 
@pytest.fixture
def learner_user_enrollment(db,learner_user,course):
    return Enrollment.objects.create(user=learner_user,course=course)

# @pytest.fixture
# def other_learner_enrollment(db,other_learner_user,course)
@pytest.fixture
def assignment_for_learner(db,learner_user_enrollment,course):
    return Assignment(course=course,
                      title="this is test assignment",
                      description="this is test description for test assignment",
                      deadline = datetime.now(timezone.utc)+timedelta(days=2))

@pytest.fixture
def api_client():
    return APIClient()