from rest_framework import serializers
from .models import Product, Review, Cart, ProductTag, ProductTag, FavoriteProduct
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['product_id', 'content', 'rating']

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
        user = self.context['request'].user
        return Review.objects.create(product=product, user=user, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        exclude = ['created_at', 'updated_at'] 
        model = Product

# class PositiveIntegerField(serializers.Serializer):
#       def raxac(self,value):
#         Product.objects.get(Product=value)
#         if value < 1:
#             raise serializers.ValidationError("it is not possible")
#         return value
    
class CartModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Cart
            fields = "__all__"
#     products = serializers.PrimaryKeyRelatedField(
#         queryset=Product.objects.all(), many=True
#     )
#     quantity = serializers.IntegerField()

#     def validate_quantity(self, value):
#         if value < 1:
#             raise serializers.ValidationError("Quantity must be at least 1.")
#         return value

# class TagSerializer(serializers.Serializer):
#     product_id = serializers.IntegerField(write_only=True)
#     tag_name = serializers.CharField()

#     def validate_product_id(self, value):
#         if not Product.objects.filter(id=value).exists():
#             raise serializers.ValidationError("Invalid product_id. Product does not exist.")
#         return value

#     def validate(self, data):
#         product = Product.objects.get(id=data['product_id'])
#         if product.tags.filter(name=data['tag_name']).exists():
#             raise serializers.ValidationError("Tag name must be unique for this product.")
#         return data

#     def create(self, validated_data):
#         product = Product.objects.get(id=validated_data['product_id'])
#         tag, created = ProductTag.objects.get_or_create(name=validated_data['tag_name'])
#         product.tags.add(tag)
#         return tag

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

class ProductModelTag(serializers. ModelSerializer):
        class Meta:
            model = ProductTag
            fields = "__all__"

     

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

