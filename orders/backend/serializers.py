from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db import transaction
from backend.models import User, Shop, Category, Product , Parameter, Cart, Order, OrderItem


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализатор регистрации пользователя и создания нового. """

    token = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(
        max_length=100,
        min_length=5,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    """ 
    Сериализотр для аторизации пользователя. С методом validate который проверяет
    валиден ли пользовтель или нет, по email и password. С несколькими обработаными исключениями.
    Не предоставлен email или password, нет такого пользоветля с таким email и password и проверка 
    активен ли пользователь (is_active).
    """
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # передаем email как username, так как в модели пользователя USERNAME_FIELD = email.
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'username': user.username,
            'email': user.email,
            'token': user.token
        }
    

class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор обновления пользователя """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление пользователя. """
        # удаляем поле password для использования специальной функци Django
        # (set_password)
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
    

class ShopSerializer(serializers.ModelSerializer):
    """ Сериализатор для представления ShopView """

    class Meta:
        model = Shop
        fields = ('id', 'title', 'address', 'categories')


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для представления CategoryView"""

    class Meta:
        model = Category
        fields = ('id', 'name', 'shops')

class ParameterSerializer(serializers.ModelSerializer):
    """ Сериализатор для представления ParameterView"""

    class Meta:
        model = Parameter
        fields = ('product','price', 'description', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор для представления ProductView """

    parameters = ParameterSerializer(many=True, read_only=True,)
    class Meta:
        model = Product
        fields = ('id', 'name', 'сategory', 'shop', 'parameters', 'product_infos')


class CartSerializer(serializers.ModelSerializer):
    """ Serializer для представления CartViewSet """

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity'] 
        read_only_fields = ['user'] 


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer для представления OrderViewSet """
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_timestamp', 'order_items']        
