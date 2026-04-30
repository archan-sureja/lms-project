from django.urls import reverse
from courses.models import Enrollment
class TestEnrollmentsLearner:
    def test_enrollment_list(self,api_client,learner_user):
        url = reverse("enrollment-list-create")
        api_client.force_authenticate(user=learner_user)
        res = api_client.get(url)
        assert res.status_code == 403


    def test_create_enrollment_with_allowed_course(self,api_client,learner_user,course):
        url = reverse("enrollment-list-create")
        api_client.force_authenticate(user=learner_user)
        res = api_client.post(url,{
            "course": course.id,
            "user" : learner_user.id 
        })
        assert res.status_code == 201
        print(res.data)
        assert Enrollment.objects.filter(user=learner_user,course=course).count()==1 
    
    def test_create_enrollment_with_not_allowed_dept(self,api_client,learner_user,not_allowed_dept_course):
        url = reverse("enrollment-list-create")
        api_client.force_authenticate(user=learner_user)
        res = api_client.post(url)
        assert res.status_code == 400

    def test_create_enrollment_with_not_allowed_level(self,api_client,learner_user,not_allowed_level_course):
        url = reverse("enrollment-list-create")
        api_client.force_authenticate(user=learner_user)
        res = api_client.post(url)
        assert res.status_code == 400
        print(res.data)



