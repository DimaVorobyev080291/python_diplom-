from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from backend.models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, **kwargs):
    print("Объект сохранён !!!!!!!!!!!!!!!!!!!")
    send_mail(
        subject='Добро пожаловать в Магазин ',
        message=f'Привет! Рады видеть вас !',
        from_email='dima02081991@mail.ru',
        recipient_list=['dimaV02081991@ya.ru']
    )
    print(234)
   