from django.urls import reverse 
from assignments.models import Assignment
from courses.models import Enrollment 
from datetime import datetime , timedelta, timezone 
class TestAssignmentsLearner:
    def test_list_assignment(self,api_client,learner_user,course):
        Enrollment.objects.create(user=learner_user,course=course)
        assignment = Assignment.objects.create(
                    course=course,
                    title="this is test title",
                    description="this is test description",
                    deadline=datetime.now(timezone.utc)+timedelta(days=2))
        url = reverse("assignment-list")
        api_client.force_authenticate(user=learner_user)
        res = api_client.get(url)
        assert res.status_code == 200
        assert res.data[0]['id'] == assignment.id 
        

    def test_create_assingment_not_allowed(self,api_client,learner_user):
        url = reverse("assignment-list")
        api_client.force_authenticate(user=learner_user)
        res = api_client.post(url,{
            "some-data":"some-value"
        })
        assert res.status_code == 403 
    

    def test_update_assingment_not_allowed(self,api_client,learner_user):
        url = reverse("assignment-detail",args=[1])
        api_client.force_authenticate(user=learner_user)
        res = api_client.put(url,{
            "some-data":"some-value"
        })
        assert res.status_code == 403 

    def test_delete_assingment_not_allowed(self,api_client,learner_user):
        url = reverse("assignment-detail",args=[1])
        api_client.force_authenticate(user=learner_user)
        res = api_client.delete(url,)
        assert res.status_code == 403 