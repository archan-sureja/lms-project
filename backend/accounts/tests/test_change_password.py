from django.urls import reverse 
from accounts.models import User
class TestChangePassword:

    def test_change_password_with_correct_input(self,api_client,user):
        url = reverse("change_password")
        api_client.force_authenticate(user=user)
        res = api_client.patch(url,{
            "old_password":"password@1234",
            "new_password":"newpassword@1234"
        })
        assert res.status_code == 204 
        assert User.objects.get(pk=user.id).check_password("newpassword@1234")
        assert res.data is None
    
    def test_change_password_with_incorrect_input(self,api_client,user):
        url = reverse("change_password")
        api_client.force_authenticate(user=user)
        res = api_client.patch(url,{
            "old_password":"wrongpassword",
            "new_password":"newpassword@1234"
        })
        assert res.status_code == 400
    
    def test_change_password_with_incorrect_jwt_token(self,api_client,user):
        url = reverse("change_password")
        api_client.credentials(HTTP_AUTHORIZATION='Bearer ' +"thisisfalsejwttoken")
        res = api_client.patch(url,{
            "old_password":"password@1234",
            "new_password":"newpassword@1234"
        })
        assert res.status_code == 401