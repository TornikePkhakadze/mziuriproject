from rest_framework import serializers
from categories.models import Category , CategoryImage
from products.serializer import ProductSerializer



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ["id", "images", "category", "is_active"]

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many= True, read_only = True)
    images = CategoryImageSerializer(many=True, read_only = True)

    class Meta:
        model =  Category
<<<<<<< HEAD
        fields = ["id", "name", "products", "images"]
=======
        fields = ["id", "name", "products", "images"]
>>>>>>> 527e887b3351317a5571ab6d30a504a00479768d
