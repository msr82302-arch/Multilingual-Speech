from rest_framework.permissions import BasePermission


class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Professor").exists()


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Student").exists()