from django.db import models
from config.util_models.models import TimeStampdModels


class Category(TimeStampdModels):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField('products.Product', related_name='categories')

    def __str__(self):
        return f'item_name:{self.name}'

class CategoryImage(TimeStampdModels):
    category = models.ForeignKey('categories.Category', related_name='images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='categories/')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'item_name:{self.name}'