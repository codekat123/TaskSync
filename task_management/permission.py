from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
     def has_permission(self,request,view):
          return request.user and request.user.role == 'Manager'

class IsTeamLeader(BasePermission):
     def has_permission(self,request,view):
          return request.user and request.user.role == 'teamleader'

class IsEmployee(BasePermission):
     def has_permission(self,request,view):
          return request.user and request.user.role == 'employee'