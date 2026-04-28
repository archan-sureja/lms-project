from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action 
from rest_framework.response import Response 
from rest_framework import generics 
from rest_framework import status
from accounts.permissions import IsInstructor, IsLearner
from .models import Assignment, Submission, SubmissionGrade
from .serializers import (
    AssignmentCreateUpdateSerializer,
    AssignmentSerializer,
    SubmissionCreateSerializer,
    SubmissionSerializer,
    SubmissionUpdateSerializer,
    SubmissionGradeSerializer,
    SubmissionGradeCreateSerializer
)


class AssignmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsInstructor]
    serializer_class = AssignmentCreateUpdateSerializer

    def get_queryset(self):
        if self.request.user.role == "LEARNER" and self.action == "list":
            print("DEBUG: changing queryset for learner")
            assignments = Assignment.objects.filter(
                course__in=self.request.user.enrollments.values_list(
                    "course", flat=True
                )
            )
        else:
            assignments = Assignment.objects.filter(
                course__instructor=self.request.user
            )
        course = self.request.query_params.get("course", None)
        if course:
            assignments = assignments.filter(course=course)
        return assignments

    def get_permissions(self):
        if self.request.user.role == "LEARNER" and self.action == "list":
            print("DEBUG: changing permission for learner")
            self.permission_classes = [IsAuthenticated, IsLearner]
        return super().get_permissions()

    def get_serializer(self, *args, **kwargs):
        if self.request.user.role == "LEARNER" and self.action == "list":
            print("DEBUG: changing serializer for learner")
            self.serializer_class = AssignmentSerializer
        return super().get_serializer(*args, **kwargs)

    def perform_destroy(self, instance):
        if instance.course.instructor != self.request.user:
            raise PermissionDenied(
                detail="only instructor can delete assignments",
                code=status.HTTP_403_FORBIDDEN,
            )
        return super().perform_destroy(instance)


class SubmissionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsLearner]
    serializer_class = SubmissionCreateSerializer

    def get_queryset(self):
        if self.request.user.role == "INSTRUCTOR" and self.action == "list":
            submissions = Submission.objects.filter(
                assignment__course__instructor=self.request.user
            )
        else:
            submissions = Submission.objects.filter(submitted_by=self.request.user)
        assignment = self.request.query_params.get("assignment", None)
        if assignment:
            submissions = submissions.filter(assignment=assignment)
        return submissions

    def get_serializer(self, *args, **kwargs):
        if self.request.user.role == "LEARNER" and self.action == "list":
            self.serializer_class = SubmissionSerializer
        elif self.action == "update":
            self.serializer_class = SubmissionUpdateSerializer
        return super().get_serializer(*args, **kwargs)
    def get_permissions(self):
        if self.request.user.role == "INSTRUCTOR" and (self.action == "list" or self.action=="grade"):
            self.permission_classes = [IsAuthenticated,IsInstructor]
        else:
            self.permission_classes = [IsAuthenticated,IsLearner]
        return super().get_permissions()
    def perform_create(self, serializer):
        return serializer.save(submitted_by=self.request.user)

    def perform_destroy(self, instance):
        if instance.submitted_by != self.request.user:
            raise PermissionDenied(
                detail="only owner can perform delete", code=status.HTTP_403_FORBIDDEN
            )
        return super().perform_destroy(instance)

    @action(detail=True,methods=['POST'])
    def grade(self,request,pk=None):
        submission = self.get_object()
        grade = getattr(submission,"grade",None)
        if grade :
            serializer = SubmissionGradeCreateSerializer(grade,data=request.data,partial=True)
        else:
            serializer = SubmissionGradeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(submission=submission)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SubmissionGradeListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionGradeSerializer 
    def get_queryset(self):
        if self.request.user.role == "LEARNER":
            return SubmissionGrade.objects.filter(submission__submitted_by=self.request.user)
        return SubmissionGrade.objects.filter(submission__assignment__course__instructor=self.request.user)
    