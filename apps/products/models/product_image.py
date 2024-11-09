from django.db import models



class ProductImage(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='discount/images/%Y/%m/%d/',
                              # validators=[discount_image_size]
                              )
    ordering_number = models.PositiveSmallIntegerField()

