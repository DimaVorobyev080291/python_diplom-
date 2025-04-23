from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Проверка на права пользователей (кто создал запись тот и имеет прова на действия с ней )
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
    
   