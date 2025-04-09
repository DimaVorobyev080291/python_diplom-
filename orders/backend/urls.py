from django.urls import path
# from rest_framework.routers import DefaultRouter
from backend.views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, ShopView, \
    CategoryView, ProductView


from rest_framework.routers import DefaultRouter

from backend.views import CartViewSet

router = DefaultRouter()
router.register('cart', CartViewSet)

    
app_name = 'authentication'
urlpatterns = [
    path('users', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/', UserRetrieveUpdateAPIView.as_view()),
    path('shops/', ShopView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('product/', ProductView.as_view()),
    # path('cart/', CartListCreateView.as_view()),
    # path('cart/<int:pk>/', CartUpdateAPIView.as_view()),
    # path('cart/<int:pk>/', CartDestroyAPIView.as_view()),

] + router.urls
