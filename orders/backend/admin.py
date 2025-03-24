from django.contrib import admin
from .models import Shop, User, Category
from django.forms import BaseInlineFormSet

def summary(obj) -> str:
    """ Метод конвертации столбцов в короткую запись """
    if len(obj)> 30:
        return f"{obj[:20]}..."
    return obj


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """ Админка модели Shop """
    list_display = ['id', 'title', 'address_summary']

    @admin.display(description='Адрес')
    def address_summary(self, obj) -> str:
        address = summary(obj.address)
        return address 
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Админка модели User """
    list_display = ['id', 'username', 'email']


@admin.register(Category)
class CategotyAdmin(admin.ModelAdmin):
    """ Админка модели Категория """
    list_display = ['id', 'name']
    filter_horizontal = ['shops']