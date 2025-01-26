from django.contrib import admin
from products.models import Product, ProductsImage, ProductTag, FavoriteProduct, Review, Cart


class ImageInLine(admin.TabularInline):
    model = ProductsImage
    extra = 0

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]


admin.site.register(ProductsImage)
admin.site.register(ProductTag)
admin.site.register(FavoriteProduct)
admin.site.register(Review)
admin.site.register(Cart)
