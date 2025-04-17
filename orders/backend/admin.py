from django.contrib import admin
from .models import Shop, User, Category, Product, Parameter, Cart, Order, OrderItem
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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Админка модели Продук """
    list_display = ['id', 'name', 'сategory', 'shop']


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    """ Админка модели Параметры """
    list_display = ['id', 'product', 'price', 'description', 'quantity']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """ Админка модели Корзина покупателя  """
    list_display = ['id', 'user', 'product', 'quantity', 'created_timestamp']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Админка модели Заказ """
    list_display = ['id', 'user', 'status', 'created_timestamp']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """ Админка модели позиции в заказе """
    list_display = ['id', 'order', 'product', 'quantity', 'created_timestamp']