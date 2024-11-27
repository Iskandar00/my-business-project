from django.db import models


class ProductFeature(models.Model):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='product_features')

    feature_value = models.ForeignKey(
        'features.FeatureValue',
        on_delete=models.PROTECT,
        related_name='product_features')

    def __str__(self):
        return f"{self.product}"
