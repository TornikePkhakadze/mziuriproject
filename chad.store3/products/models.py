from django.db import models
from config.util_models.models import TimeStampdModels
from products.choices import Currency
from django.core.validators import MaxValueValidator, MinValueValidator
from config.utils.image_validators import validate_image_size, validate_image_resolution, validate_image_count


class Product(TimeStampdModels):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.GEL)
    quantity = models.PositiveSmallIntegerField()
    user = models.ForeignKey('users.User', null=True,on_delete=models.CASCADE, related_name="products")
    
    def __str__(self):
        return f'item_name:{self.name}'

class ProductTag(TimeStampdModels):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('products.Product', related_name='tags')

    def __str__(self):
        return f'item_tag:{self.name}'

class Review(TimeStampdModels):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
        unique_together = ["product", "user"]


class Cart(TimeStampdModels):
    products = models.ManyToManyField('products.Product', related_name='carts')
    user = models.OneToOneField('users.User', related_name='cart', on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="itmes", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_ietms", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_of_addition = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} items"
    
    def total_price(self):
        return self.quantity * self.price_at_of_addition


class FavoriteProduct(TimeStampdModels):
    products = models.ForeignKey('products.Product', related_name='favorite_products', on_delete=models.CASCADE)
    user = models.OneToOneField('users.User', related_name='favorite_products', on_delete=models.SET_NULL, null=True, blank=True)

class ProductsImage(TimeStampdModels):
    product = models.ForeignKey('products.Product',related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', validators=[validate_image_resolution,validate_image_size])
     
    def clean(self):
        if self.product_id:
            validate_image_count(self.product_id)
        super().clean

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        