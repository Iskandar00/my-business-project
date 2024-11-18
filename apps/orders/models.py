from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError
"""
{
    "buyer_name": "kimdir",
    "phone_number": "+998907654321",
    "area": 1,
    "product_count": 4
}
"""


class Order(models.Model):
    link = models.ForeignKey('links.Link', on_delete=models.SET_NULL, null=True)

    class AreaChoices(models.IntegerChoices):
        TOSHKENT = 1, 'Toshkent'
        QORAQALPOGISTON = 14, 'Qoraqalpogiston'
        QASHQADARYO = 11, 'Qashqadaryo'
        SIRDAYO = 2, 'Sirdaryo'
        JIZZAX = 3, 'Jizzax'
        FARGONA = 5, 'Fargona'
        NAMANGAN = 6, 'Namangan'
        ANDIJON = 7, 'Andijon'
        BUXORO = 8, 'Buxoro'
        XORAZM = 9, 'Xorazm'
        NAVOIY = 10, 'Navoiy'
        SURXONDARYO = 12, 'Surxondaryo'
        SAMARQAND = 13, 'Samarqand'

    class StatusChoices(models.IntegerChoices):
        YANGI = 1, 'YANGI'
        DASTAVKAGA_TAYYOR = 2, 'DASTAVKAGA_TAYYOR'
        YETKAZILMOQDA = 3, 'YETKAZILMOQDA'
        QAYTA_QUNGIROQ = 4, 'QAYTA_QUNGIROQ'
        YETKAZIB_BERILDI = 5, 'YETKAZIB_BERILDI'

    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.YANGI)
    admin = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, blank=True, null=True)
    admin_money = models.DecimalField(max_digits=20, decimal_places=2)
    product_count = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    buyer_name = models.CharField(max_length=50)
    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r"^\+998\d{9}$",
                message="Example: +998 XXXXXXXXX",
                code="uzb_phone_number_validation"
            )
        ]
    )
    area = models.IntegerField(choices=AreaChoices.choices)
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.link:
            self.admin = self.link.user
            self.product = self.link.product
            self.admin_money = self.product.admin_money * self.product_count
        else:
            raise ValidationError("create_link must have associated user and product.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} for {self.buyer_name} from {self.area}"
