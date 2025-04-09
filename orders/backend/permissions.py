from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Проверка на права для модели Cart просмотреть может любой со всеми остальными действиями 
    проверяем что User такой же что и создал эту Cart
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user == obj.user