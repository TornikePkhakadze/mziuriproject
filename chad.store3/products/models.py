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
    
    def __str__(self):
        return f'item_name:{self.name}'

class ProductTag(TimeStampdModels):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('products.Product', related_name='product_tags')

    def __str__(self):
        return f'item_tag:{self.name}'

class Review(TimeStampdModels):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])


class Cart(TimeStampdModels):
    products = models.ManyToManyField('products.Product', related_name='carts')
    user = models.OneToOneField('users.User', related_name='cart', on_delete=models.CASCADE)

class FavoriteProduct(TimeStampdModels):
    products = models.ForeignKey('products.Product', related_name='favorite_products', on_delete=models.CASCADE)
    user = models.OneToOneField('users.User', related_name='favorite_products', on_delete=models.SET_NULL, null=True, blank=True)

class ProductsImage(TimeStampdModels):
    product = models.ForeignKey('products.Product',related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
     
