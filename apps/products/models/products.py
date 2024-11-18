from django.db import models
from django.core.exceptions import ValidationError

from apps.general.unique_id import generate_unique_id


class Product(models.Model):
    main_category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,
        related_name='products',
        blank=True, null=True)

    sub_category = models.ForeignKey(
        'categories.SubCategory',
        on_delete=models.PROTECT,
        related_name='products',
        blank=True, null=True)

    id_generate = models.CharField(
        unique=True,
        max_length=8,
        editable=False,
        default=generate_unique_id
    )
    name = models.CharField(max_length=700)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)

    in_stock = models.PositiveSmallIntegerField(default=0)
    admin_money = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    delivery_price = models.PositiveIntegerField(default=30000)

    is_active = models.BooleanField(default=True)
    like_counts = models.IntegerField(default=0)
    view_counts = models.IntegerField(default=0)
    comment_counts = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name

    def clean(self):
        if bool(self.main_category) + bool(self.sub_category) != 1:
            raise ValidationError("Choose either main_category or sub_category, only one of the two.")