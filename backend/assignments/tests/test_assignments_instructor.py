from django.urls import reverse 
from assignments.models import Assignment
from datetime import datetime , timedelta , timezone 
class TestAssignmentsInstructor:

    def test_assignment_list(self,api_client,user,assignment):
        
        url = reverse('assignment-list')
        api_client.force_authenticate(user=user)
        res = api_client.get(url)
        assert res.status_code == 200 
        assert res.data[0]['id'] == assignment.id 
    
    def test_create_assignment(self,api_client,user,course):
        url = reverse('assignment-list')
        api_client.force_authenticate(user=user)
        res = api_client.post(url,{
            "course":course.id,
            "title":"this is title",
            "description":"this is description",
            "deadline": datetime.now(timezone.utc) + timedelta(days=2)
        }) 
        assert res.status_code == 201
    
    # def test_udpate_assignment_as_creator(self,api_client,user,course):
    #     assignment = Assignment.objects.create(
    #         course=course,
    #         title="this is title",
    #         description="this is test description",
    #         deadline=datetime.now(timezone.utc)+timedelta(days=2))
    #     url = reverse('assignment-detail',args=(assignment.id,))
    #     update_title = "this is new title"
    #     api_client.force_authenticate(user=user)
    #     res = api_client.put(url,{
    #         "title": update_title , 
    #     })
    #     assert res.status_code == 201 
    def test_update_assignment_as_not_creator(self):
        pass 

    def test_delete_assignment_as_creator(self,api_client,user,assignment):
        url = reverse("assignment-detail",args=(assignment.id,))
        api_client.force_authenticate(user=user)
        res = api_client.delete(url)
        assert res.status_code == 204 

    def test_delete_assignment_as_not_creator(self,api_client,other_instructor,assignment):
        url = reverse("assignment-detail",args=(assignment.id,))
        api_client.force_authenticate(user=other_instructor)
        res = api_client.delete(url)
        assert res.status_code == 404 