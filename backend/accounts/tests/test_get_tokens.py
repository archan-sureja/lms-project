
from django.urls import reverse


class TestGetObtainTokenPair:
    def test_get_tokens_endpoint_with_valid_credentials(self,client,user):
        url = reverse("token_obtain_pair")
        data = {
            "username":"testuser",
            "password":"password@1234"
        }
        response = client.post(url,data)
        assert response.status_code == 200 
        assert response.data['access'] 
        assert response.data['refresh']
        
    def test_get_token_endpoint_with_invalid_credentials(self,client,user):
        url = reverse("token_obtain_pair")
        invalid_data = {
            "username":"testuser",
            "password":"1111",
            "some_data":"some_data"
        }
        response = client.post(url,invalid_data)
        assert response.status_code == 401 

    def test_get_token_enpoint_with_no_credentials(self,client,user):
        url = reverse("token_obtain_pair")
        no_cred_data = {
            "username":"",
            "password":"",
        }
        response = client.post(url,no_cred_data)
        assert response.status_code == 400

