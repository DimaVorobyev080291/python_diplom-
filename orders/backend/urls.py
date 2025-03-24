from django.urls import path

from backend.views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, ShopView, \
    CategoryView, ProductView
    

app_name = 'authentication'
urlpatterns = [
    path('users', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/', UserRetrieveUpdateAPIView.as_view()),
    path('shops/', ShopView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('product/', ProductView.as_view()),

]