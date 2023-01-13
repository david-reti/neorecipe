from rest_framework.permissions import BasePermission

class OnlyStaffCanCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_staff
        return True

class OnlyStaffCanUpdate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PUT' or request.method == 'PATCH':
            return request.user.is_staff
        return True

class OnlyStaffCanDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_staff
        return True