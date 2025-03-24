from django.db import models
import jwt
from datetime import datetime, timedelta
from django.conf import settings 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Shop(models.Model):
    """ Класc модели магазин (Shop) """

    title = models.CharField(max_length=100, verbose_name='Название')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    # products = models.ManyToManyField(
    #     Product,
    #     through='StockProduct',
    #     related_name='stocks',
    # )

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-title',)

    def __str__(self):
        return self.title
    

class UserManager(BaseUserManager):

    """ Кастомный класс Manager. Унаследовавшись от BaseUserManager. """

    def create_user(self, username, email, password=None):

        """ Метод создает и возвращает пользователя с имэйлом, паролем и именем. """

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, username, email, password):

        """ Создает и возввращет пользователя с привилегиями суперадмина. """

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    

class User(AbstractBaseUser, PermissionsMixin):

    """ Класс модели пользователь (User) """

    username = models.CharField(db_index=True, max_length=100, verbose_name='Имя пользователя')
    email = models.EmailField(db_index=True, unique=True, verbose_name='Электронная почта')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 100 день от создания
        """
        dt = datetime.now() + timedelta(days=100)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)

class Category(models.Model):
    """Класс модели категория товара """

    name = models.CharField(max_length=100, verbose_name='Название')
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('name',)

    def __str__(self):
        return self.name