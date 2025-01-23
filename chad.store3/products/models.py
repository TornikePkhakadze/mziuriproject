from django.db import models
from config.util_models.models import TimeStampdModels
from products.choices import Currency
from django.core.validators import MaxValueValidator, MinValueValidator

class Product(TimeStampdModels):

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.GEL)
    quantity = models.PositiveSmallIntegerField()

class ProductTag(TimeStampdModels):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('products.Product', related_name='product_tags')


class Review(TimeStampdModels):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])