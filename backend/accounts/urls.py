
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views 
urlpatterns = [
    path('api/token/',views.MyTokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name="refresh_token"),
    path('change-password/',views.ChangePasswordView.as_view(),name="change_password")
]