from django.urls import reverse 

class TestRefreshTokenEndpoint:

    def test_with_valid_refresh_token(self,client,user):
        get_token_url = reverse('token_obtain_pair')
        get_tokens_res = client.post(
            get_token_url,
            {
                "username":"testuser",
                "password":"password@1234"
            }
        )
        refresh_token = get_tokens_res.data['refresh']
        url = reverse('refresh_token')
        res = client.post(url,{
            "refresh":refresh_token
        })
        assert res.status_code == 200 
        assert res.data['access'] 

    def test_with_invalid_refresh_token(self,client):
        refresh_token = "this is invalid refresh token"
        url = reverse('refresh_token')
        res = client.post(url,{
            "refresh":refresh_token
        })
        assert res.status_code == 401 

    def test_without_refresh_token(self,client):
        url = reverse('refresh_token')
        res = client.post(url,{
            "other_then_refresh":"dummy data"
        })
        assert res.status_code == 400

