from django.urls import reverse 
from assignments.models import Assignment
from datetime import datetime , timedelta , timezone 
class TestAssignmentsInstructor:

    def test_assignment_list(self,api_client,user,course):
        assingment = Assignment.objects.create(
                    course=course,
                    title="this is title",
                    description="this is test description",
                    deadline=datetime.now(timezone.utc)+timedelta(days=2))
        url = reverse('assignment-list')
        api_client.force_authenticate(user=user)
        res = api_client.get(url)
        assert res.status_code == 200 
        assert res.data[0]['id'] == assingment.id 
    
    def test_create_assignment(self,api_client,user,course):
        url = reverse('assignment-list')
        api_client.force_authenticate(user=user)
        res = api_client.post(url,{
            "course":course.id,
            "title":"this is title",
            "description":"this is description",
            "deadline": datetime.now(timezone.utc) + timedelta(days=2)
        }) 
        assert res.status_code == 200
    
    def test_udpate_assignment_as_creator(self,api_client,user,course):
        url = reverse('assignemnt-detail',args=())
        api_client.force_authenticate(user=user)

    def test_update_assignment_as_not_creator(self):
        pass 

    def test_delete_assignment_as_creator(self):
        pass 

    def test_delete_assignment_as_not_creator(self):
        pass 