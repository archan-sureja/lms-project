from django.urls import reverse 
from courses.models import Course
class TestCoursesForInstructor:
    def test_list_courses_with_authenticated_user(self,api_client,user,courses_created_by_user):
        url = reverse("course-list")
        api_client.force_authenticate(user=user)
        res = api_client.get(url)
        assert res.status_code == 200
        assert len(res.data) == Course.objects.filter(instructor=user).count()

    def test_list_courses_with_not_auth_user(self,api_client):
        url = reverse("course-list")
        res = api_client.get(url)
        assert res.status_code == 401 

    def test_create_course_with_auth_user(self,api_client,user,tags):
        api_client.force_authenticate(user=user)
        url = reverse("course-list") 
        res = api_client.post(url,{
            "title":"test title",
            "description":"this is test description",
            "tags":[tag.id for tag in tags],
            "topics": [
                {
                    "name":'test topic 1',
                    "resource_link":"http://test.com"
                }
            ],
            "instructor":-1 #this must be ignored 
        },format="json")
        print(res.data)
        assert res.status_code == 201 
        assert res.data['instructor'] == user.username



    def test_update_course_as_creator(self,api_client,user,course):
        api_client.force_authenticate(user=user)
        url = reverse("course-detail",args=(course.id,)) 
        res = api_client.put(url,{
            "title":"test title",
            "description":"this is test description",
            "instructor":-1 #this must be ignored 
        },format="json")
        print(res.data)
        assert res.status_code == 200
        assert res.data['instructor'] == user.username
        

    def test_update_course_as_not_creator(self,api_client,other_instructor,course):
        url = reverse("course-detail",args=(course.id,))
        api_client.force_authenticate(user=other_instructor)
        res = api_client.put(url,{"some-data":"some-value"})
        assert res.status_code == 404 
        

    def test_delete_course_as_creator(self,api_client,user,course):
        url = reverse("course-detail",args=(course.id,))
        api_client.force_authenticate(user=user)
        res = api_client.delete(url)
        assert res.status_code == 204 
        
    
    def test_delete_course_as_not_creator(self,api_client,other_instructor,course):
        url = reverse("course-detail",args=(course.id,))
        api_client.force_authenticate(user=other_instructor)
        res = api_client.delete(url)
        assert res.status_code == 404

    def test_detail_course_as_creator(self,api_client,user,course):
        url = reverse("course-detail",args=(course.id,))
        api_client.force_authenticate(user=user)
        res = api_client.get(url)
        assert res.status_code == 200
        assert res.data['instructor'] == user.username 
        

    def test_detail_course_as_not_creator(self,api_client,other_instructor,course):
        url = reverse("course-detail",args=(course.id,))
        api_client.force_authenticate(user=other_instructor)
        res = api_client.get(url)
        assert res.status_code == 404 