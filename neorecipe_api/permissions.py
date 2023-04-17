from rest_framework.permissions import BasePermission

class AnyoneCanView(BasePermission):
    def has_permission(self, request, view):
        return True

class OnlyStaffCanCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_staff
        return True

class AnyoneCanCreate(BasePermission):
    def has_permission(self, request, view):
        return True

class OnlyStaffCanUpdate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PUT' or request.method == 'PATCH':
            return request.user.is_staff
        return True

class AnyoneCanUpdate(BasePermission):
    def has_permission(self, request, view):
        return True

class OnlyStaffCanDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_staff
        return True
    
class AnyoneCanDelete(BasePermission):
    def has_permission(self, request, view):
        return True

class OwnerAndStaffCanUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT' or request.method == 'POST':
            return request.user == obj.creator or request.user.is_staff
        return True

class OwnerAndStaffCanDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user == obj.creator or request.user.is_staff
        return True

class OnlyCurrentUserAndStaffCanView(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user == obj or request.user.is_staff
        return True

class OnlyCurrentUserAndStaffCanUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
            return request.user == obj or request.user.is_staff
        return True
