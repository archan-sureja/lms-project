from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .serializers import CourseSerializer , CourseDetailSerializer
from .models import Course
from .permissions import IsLearner

class CourseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer 

    def get_queryset(self):
        if self.request.user.role == "INSTRUCTOR":
            return Course.objects.filter(instructor=self.request.user)
        return Course.objects.filter(
            Q(allowed_depts= self.request.user.employee_profile.department) & 
            Q(allowed_levels= self.request.user.employee_profile.level)
        ).exclude(id__in=self.request.user.enrollments.values_list("course_id",flat=True))
    
    def get_permissions(self):
         if self.action == "enrolled":
              self.permission_classes = [IsAuthenticated,IsLearner]
         elif self.action == "retrieve":
              self.permission_classes = [IsAuthenticated]
         return super().get_permissions() 
    
    def get_serializer(self, *args, **kwargs):
         if self.action == "retrieve":
              self.serializer_class = CourseDetailSerializer
         return super().get_serializer(*args, **kwargs)
    @action(detail=False,methods=['GET'])
    def enrolled(self,request):
            print("DEBUG : ",self.permission_classes)
            self.queryset = Course.objects.filter(id__in=self.request.user.enrollments.values_list("course_id",flat=True))
            serializer = self.get_serializer(self.queryset,many=True)
            return Response(serializer.data)
  
