from django.db import models
from config.util_models.models import TimeStampdModels


class Category(TimeStampdModels):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField('products.Product', related_name='categories')

class CategoryImage(TimeStampdModels):
    category = models.ForeignKey('categories.Category', related_name='images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='categories/')