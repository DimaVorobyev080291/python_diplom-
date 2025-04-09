from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from backend.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from backend.renderers import UserJSONRenderer
from backend.serializers import RegistrationSerializer, LoginSerializer, UserSerializer, ShopSerializer, \
    CategorySerializer, ProductSerializer, CartSerializer
from backend.models import Shop, Category, Product, Cart
from django_filters.rest_framework import DjangoFilterBackend


class RegistrationAPIView(APIView):
    """ Класс регистрации пользователий (аутентифицированным и нет). """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)


    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LoginAPIView(APIView):
    """ Класс для авторизации User"""

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Класс получения и обновления пользоветеля """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ShopView(ListAPIView):
    """ Класс для просмотра модели Shop """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class CategoryView(ListAPIView):
    """ Класс для просмотра модели Category """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(ListAPIView):
    """ Класс для просмотра модели product. С возможностью фильтрации. """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop', 'сategory']


class CartViewSet(ModelViewSet):
    """ViewSet с полныс CRUD функционалом для таблице Cart. С возможностью фильтрации. """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get_permissions(self):
        """
        Получение прав для действий c моделью Cart авторизированый пользователь может создать, просмотреть
        корзину. Для измения и удаления пользователь должен совпадать с тем же пользователем что и создал 
        эту корзину
        """
        if self.action in ['create', 'list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []