from django.urls import reverse 
class TestCoursesLeaner:

    # def test_allowed_course_list(self,allowed_courses_learner_user):
    #     pass 

    # def test_enrolled_course_list(self,enrolled_courses_learner_user):
    #     pass 

    def test_create_not_allowed(self,api_client,learner_user):
        api_client.force_authenticate(user=learner_user)
        url = reverse('course-list')
        res = api_client.post(url,{
            "some_data":"random value"
        })
        assert res.status_code == 403 
    
    def test_update_not_allowed(self,api_client,learner_user,course):
        api_client.force_authenticate(user=learner_user)
        url = reverse('course-detail',args=(course.id,))
        res = api_client.put(url,{
            "some_data":"random value"
        })
        assert res.status_code == 403 
    
    def test_delete_not_allowed(self,api_client,learner_user,course):
        api_client.force_authenticate(user=learner_user)
        url = reverse('course-detail',args=(course.id,))
        res = api_client.delete(url)
        assert res.status_code == 403 