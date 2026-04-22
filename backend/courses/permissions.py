from rest_framework import permissions 

class IsLearner(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.role == "LEARNER")
        return request.user.role == "LEARNER"

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.role == "INSTRUCTOR")
        return request.user.role == "INSTRUCTOR"

