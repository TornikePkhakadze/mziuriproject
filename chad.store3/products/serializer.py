from rest_framework import serializers
from .models import (Product, Review,
                      Cart, ProductTag,
                        ProductTag, FavoriteProduct,
                          ProductsImage)
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
   
    class Meta:
        model = Review
        fields = ["id","user_id",'product_id', 'content', 'rating']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.pop('product_id'))
        user =  self.context["request"].user


        existing_reviews = Review.objects.filter(user=user, product=product)
        if existing_reviews.exists():
            raise serializers.ValidationError("you already have a review")

        return Review.objects.create(product=product, user=user, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        source = "tags",
        queryset = ProductTag.objects.all(),
        many = True,
        write_only = True,
    )
    class Meta:
        model = Product
        fields = ["id","name", "tags", "reviews", "description", "price", "currency","quantity", "tag_ids"]

    def create(self, validated_data):
        tags = validated_data.pop("tags",[])
        product = Product.objects.create(**validated_data)
        product.tags.set(tags)
        return product

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.set(tags)
            return super().update(instance)

class CartModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Cart
            fields = "__all__"

class FavoriteModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = FavoriteProduct
            fields = "__all__"


    # def validate_product_id(self, value):
    #     if not Product.objects.filter(id=value).exists():
    #         raise serializers.ValidationError("Wrong id Product does not exists")
    #     return value

    # def validate_user_id(self, value):
    #     if not User.objects.filter(id=value).exists():
    #         raise serializers.ValidationError("Wrong id User does not exists")
    #     return value

    # def create(self, validated_data):
    #     user = User.objects.get(id=validated_data['user_id'])
    #     product = Product.objects.get(id=validated_data['product_id'])

    #     user.favorites.add(product)  
    #     return product

class FavoriteProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    product_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = FavoriteProduct    
        fields = ["id", "user", "product_id", "products"]
        read_only_fields = ["id", "products"]

    def validate_product_id(seld,value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("given product_id does not exist")
        return value     
    
    def create(self, validated_data):
        user = validated_data.pop("user")
        product_id = validated_data.pop("product_id")
        product = Product.objects.get(id=product_id)
        favorite_product, created = FavoriteProduct.objects.get_or_create(user=user, product=product)

        if not created:
             raise serializers.ValidationError("product with id does not exist")
        return validated_data
     
class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default= serializers.CurrentUserDefault())
    products = ProductSerializer(many=True, read_only = True)
    product_ids = serializers.PrimaryKeyRelatedField(
        source="products",
        queryset=Product.objects.all(),
        write_only=True,
        many=True
    )

    class Meta:
        model = Cart
        fields = ["product_ids", "user", "products"]

    def create(self, validated_data):
        user = validated_data.pop("user")
        products = validated_data.pop("products")

        cart, _ = Cart.objects.get_or_create(user=user)

        cart.products.add(*products)

        return cart

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ["id","name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImage
        fields = ["id", "image", "product"]