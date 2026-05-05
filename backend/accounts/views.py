from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer , ChangePasswordSerializer , DepartmentSerializer , LevelSerializer , UserProfileSerializer
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView 
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Department , Level
from rest_framework.viewsets import ReadOnlyModelViewSet

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]
    def get_object(self):
        return self.request.user  

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data,
            partial=True  
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        user = self.request.user 
        serializer = UserProfileSerializer(user)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
class DepartmentViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.exclude(pk=1)
    serializer_class = DepartmentSerializer  

class LevelViewSet(ReadOnlyModelViewSet):
    queryset = Level.objects.exclude(pk=1)
    serializer_class = LevelSerializer

