from django.urls import reverse 
from courses.models import Enrollment
class TestEnrollmentsInstructor:

    def test_create_enrollments_not_allowed(self,api_client,user):
        url = reverse('enrollment-list-create')
        api_client.force_authenticate(user=user)
        res = api_client.post(url,{"some_data":"random value"})
        assert res.status_code == 403 
    
    def test_list_enrollments(self,api_client,user,enrollments):
        url = reverse('enrollment-list-create')
        api_client.force_authenticate(user=user)
        res = api_client.get(url)
        assert res.status_code == 200 
        assert len(res.data) == Enrollment.objects.filter(course__instructor=user).count()