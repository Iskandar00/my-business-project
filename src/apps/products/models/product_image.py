from django.db import models



class ProductImage(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='discount/images/%Y/%m/%d/',
                              # validators=[discount_image_size]
                              )
    ordering_number = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['ordering_number']