from rest_framework import status
from django.forms import ValidationError
from django.db import transaction
from django.http import JsonResponse
import yaml
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from backend.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from backend.renderers import UserJSONRenderer
from backend.serializers import RegistrationSerializer, LoginSerializer, UserSerializer, ShopSerializer, \
    CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer
from backend.models import Shop, Category, Product,Parameter ,Cart, Order, OrderItem
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def list(self, request, *args, **kwargs):
        """Метод list переопределен, показывает только корзины(Cart) пользователя """

        user=self.request.user
        cart_items = Cart.objects.filter(user=user)
        cart = CartSerializer(cart_items, many=True)
        return Response(cart.data)


    def get_permissions(self):
        """
        Получение прав для действий c моделью Cart авторизированый пользователь может создать корзину.
        Для измения, удаления и просмотра карзины пользователь должен совподать с создателем корзины
        """
        if self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action in ['list', 'retrieve','destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
    

class OrdeViewSet(ModelViewSet):
    """
    ViewSet с полныс CRUD функционалом для таблице Order и переопределение метода create.
    С возможностью фильтрации. 
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    
    def create(self, request, *args, **kwargs):
        """
        Метод create переопределен происходит создание запис в таблице Order и одновременно запись 
        в таблицу OrderItem. Происходит измения количества товара в таблице Parameter. 
        """
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)
                order = Order.objects.create(
                    user=user
                    )
                for item in cart_items:
                    product=item.product
                    quantity=item.quantity
            
                    product_info = Parameter.objects.filter(product_id=product)
                    for item in product_info:
                        parameter_quantity = item.quantity
                        if parameter_quantity < quantity:
                            raise ValidationError(f'Недостаточное количество товара на складе.\
                                                    В наличии - {parameter_quantity}')
                        difference = parameter_quantity - quantity
                        item.quantity = difference
                        item.save(update_fields=["quantity"])

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        )
            
                cart_items.delete()
                return JsonResponse({'Status': True, 'message': 'The order has been formed'})
        except ValidationError as e:
            print(e)
            return JsonResponse({'Status': False, 'Errors': 'The order was not formed'})
        

    def list(self, request, *args, **kwargs):
        """Метод list переопределен, показывает только заказы(Order) пользователя """

        user=self.request.user
        orde_items = Order.objects.filter(user=user)
        orde = OrderSerializer(orde_items, many=True)
        return Response(orde.data)
    
        
    def get_permissions(self):
        """
        Получение прав для действий c моделью Order авторизированый пользователь может создать заказ.
        Для измения, удаления и просмотра пользователь должен совпадать с тем же пользователем что и создал 
        этот заказ
        """
        if self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action in ['list', 'destroy', 'update', 'partial_update', 'retrieve']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]  


class ImportOfGoodsUpdate(APIView):
    """ Класс для обновления прайс листа  """

    def post(self, request, *args, **kwargs):

        try:
            with open('data/data.yaml') as file:
                data = yaml.safe_load(file)

                shop = Shop.objects.create(title=data['shop'], address=data['address'], id=data['id'])
                shop.save()
                latest_shop = Shop.objects.latest('id')
                for category in data['categories']:
                    category_object = Category.objects.create(name=category['name'], id=category['id'])
                    category_object.save()
                    category_object.shops.add(latest_shop.id)

            with transaction.atomic():
                for products in data['product']:
                    product = Product.objects.create(name=products['name'],
                                                     сategory=Category.objects.get(id=products['сategory']),
                                                     shop=Shop.objects.get(id=products['shop']))

                    latest_product = Product.objects.latest('id')
                    parameters = products['parameters']
                    parameter = Parameter.objects.create(product=Product.objects.get(id=latest_product.id),
                                                         price=parameters['price'],
                                                         description=parameters['description'],
                                                         quantity=parameters['quantity'])
            
            return JsonResponse({'Status': True , 'message': 'The download was successful'})
        except:
            return JsonResponse({'Status': False, 'Errors': 'The download was not completed !!!'})     