from rest_framework import serializers
from .models import Product, Review, Cart, ProductTag
from users.models import User

class Productserializer(serializers.Serializer):
    name=serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    currency = serializers.ChoiceField(choices=['GEL','USD','EUR'])

class ReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    content = serializers.CharField()
    rating = serializers.CharField()

    def validate_product_id(self,value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value
    
    def validate_rating(self,value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating must be between 1 and 5")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        user = self.context['request'].user

        review = Review.objects.create(
            product=product,
            user=user,
            content=validated_data['content'],
            rating=validated_data['rating'],
        )
        return review
    
# class PositiveIntegerField(serializers.Serializer):
#       def raxac(self,value):
#         Product.objects.get(Product=value)
#         if value < 1:
#             raise serializers.ValidationError("it is not possible")
#         return value
    
class CartSerializer(serializers.Serializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

class TagSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    tag_name = serializers.CharField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate(self, data):
        product = Product.objects.get(id=data['product_id'])
        if product.tags.filter(name=data['tag_name']).exists():
            raise serializers.ValidationError("Tag name must be unique for this product.")
        return data

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        tag, created = ProductTag.objects.get_or_create(name=validated_data['tag_name'])
        product.tags.add(tag)
        return tag

class FavoriteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Wrong id Product does not exists")
        return value

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Wrong id User does not exists")
        return value

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        product = Product.objects.get(id=validated_data['product_id'])

        user.favorites.add(product)  
        return product