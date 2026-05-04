from rest_framework.routers import DefaultRouter 
from .views import CourseViewSet ,TagsViewSet
from django.urls import path
from .views import EnrollmentListCreateView
router = DefaultRouter()
router.register("courses",CourseViewSet,basename="course")
router.register("tags",TagsViewSet,basename="tag")
urlpatterns = [
    path("enrollments/",EnrollmentListCreateView.as_view(),name="enrollment-list-create")
]
urlpatterns += router.urls 
