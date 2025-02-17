from django.core.validators import MinValueValidator
from django.db import models



class Shop(models.Model):
    """ Клас модели магазин (Shop) """

    name = models.CharField(max_length=100, verbose_name='Название')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    # products = models.ManyToManyField(
    #     Product,
    #     through='StockProduct',
    #     related_name='stocks',
    # )

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name