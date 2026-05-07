from rest_framework.routers import DefaultRouter 
from .views import AssignmentViewSet,SubmissionViewSet,SubmissionGradeListView
from django.urls import path
router = DefaultRouter()
router.register("assignments",AssignmentViewSet,basename="assignment")
router.register("submissions",SubmissionViewSet,basename="submissions")
urlpatterns = [
    path('grades/',SubmissionGradeListView.as_view(),name="list-grade")
]
urlpatterns += router.urls 