from rest_framework import permissions 
from .models import Course 
class IsLearner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "LEARNER"

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "INSTRUCTOR"