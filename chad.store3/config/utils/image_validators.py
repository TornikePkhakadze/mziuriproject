from django.core.validators import ValidationError
from PIL import Image

from django.apps import apps

def validate_image_size(image):
    size= image.size
    limit = 5
    min_width = 300
    min_height = 300
    max_width = 4000
    max_height = 4000
    if size >= limit * 1024 * 1024:
        raise ValidationError(f'picture size cant be over {limit}mb')
    
def validate_image_resolution (image):
    min_width = 300
    min_height = 300
    max_width = 4000
    max_height = 4000

    img = Image.open(image)
    img_wight , img_height = img.size
    if img_wight >= max_width or img_height >= max_height:
        raise ValidationError("max resolution is 4000x4000")
    if img_wight <= min_width or img_height <= min_height:
        raise ValidationError("min resolution is 300x300")


def validate_image_count(product_id):
    ProductsImage = apps.get_model("products", "ProductsImage")
    max_img = 5
    count = ProductsImage.objects.filter(product_id= product_id).count()
    if count >= max_img:
        raise ValidationError("5 products max")









