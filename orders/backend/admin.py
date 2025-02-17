from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Shop
from django.forms import BaseInlineFormSet

def summary(obj) -> str:
    """ Метод конвертации столбцов в короткую запись """
    if len(obj)> 30:
        return f"{obj[:20]}..."
    return obj


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """ Админка модели Shop """
    list_display = ['id', 'name', 'address_summary']

    @admin.display(description='Адрес')
    def address_summary(self, obj) -> str:
        address = summary(obj.address)
        return address 