from rest_framework.viewsets import ModelViewSet , ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics 
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .serializers import CourseListSerializer , CourseDetailSerializer , CourseDetailLearnerSerializer , CourseCreateUpdateSerializer ,EnrollmentCreateSerializer , EnrollmentReadOnlySerializer , TagSerializer
from .models import Course , Enrollment , Tag
from accounts.permissions import IsLearner , IsInstructor

class CourseViewSet(ModelViewSet):
     permission_classes = [IsAuthenticated]
     serializer_class = CourseListSerializer 
     filter_backends = [DjangoFilterBackend, SearchFilter]
     filterset_fields = ['tags']
     search_fields = ['title', 'description']

     def get_queryset(self):
          if self.request.user.role == "INSTRUCTOR":
               return Course.objects.filter(instructor=self.request.user)
          
          allowed_courses =  Course.objects.filter(
                    (
                         Q(allowed_depts__isnull=True) |
                         Q(allowed_depts=self.request.user.employee_profile.department)
                    ),
                    (
                         Q(allowed_levels__isnull=True) |
                         Q(allowed_levels=self.request.user.employee_profile.level)
                    )
               )
          enrolled_courses = Course.objects.filter(id__in=self.request.user.enrollments.values_list('course_id',flat=True))

          if self.action=="list":
               return allowed_courses.exclude(id__in=self.request.user.enrollments.values_list('course_id',flat=True)).distinct()
          if self.action=="retrieve":
               return (allowed_courses | enrolled_courses).distinct()
          
     def get_permissions(self):
          if self.action == "enrolled":
              self.permission_classes = [IsAuthenticated,IsLearner]
          elif self.action == "retrieve":
              self.permission_classes = [IsAuthenticated]
          elif self.action in ["create","update","destroy"]:
              self.permission_classes = [IsAuthenticated,IsInstructor]
          return super().get_permissions() 
    
     def get_serializer(self, *args, **kwargs):
          if self.action == "retrieve":
               if self.request.user.role == "INSTRUCTOR":
                    self.serializer_class = CourseDetailSerializer 
               else:
                    self.serializer_class = CourseDetailLearnerSerializer
          if self.action in ["create","update","destroy"]:
               self.serializer_class = CourseCreateUpdateSerializer
          return super().get_serializer(*args, **kwargs)
    
     @action(detail=False,methods=['GET'])
     def enrolled(self,request):
          self.queryset = Course.objects.filter(id__in=self.request.user.enrollments.values_list("course_id",flat=True))
          serializer = self.get_serializer(self.queryset,many=True)
          return Response(serializer.data)


     def perform_create(self, serializer):
          serializer.save(instructor=self.request.user)
     
     def perform_update(self,serializer):
          serializer.save(instructor=self.request.user)
     
class EnrollmentListCreateView(generics.ListCreateAPIView):
     permission_classes = [IsAuthenticated,IsInstructor]
     serializer_class = EnrollmentReadOnlySerializer

     def get_permissions(self):
          if self.request.method == "POST":
               self.permission_classes = [IsAuthenticated,IsLearner]
          return super().get_permissions()
     
     def get_queryset(self):
          if self.request.method == "GET":
               enrollments = Enrollment.objects.filter(course__instructor=self.request.user)
               course_id  = self.request.query_params.get('course')
               if course_id is not None:
                    enrollments = enrollments.filter(course=course_id)
               return enrollments 
          return Enrollment.objects.all()
     
     def get_serializer(self, *args, **kwargs):
          if self.request.method == "POST":
               self.serializer_class = EnrollmentCreateSerializer
          return super().get_serializer(*args, **kwargs)

     def perform_create(self, serializer):
          serializer.save(user=self.request.user)
     
class TagsViewSet(ReadOnlyModelViewSet):
     queryset = Tag.objects.all()
     serializer_class = TagSerializer 