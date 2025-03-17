from rest_framework import serializers
from django.contrib.auth import authenticate
from backend.models import User


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