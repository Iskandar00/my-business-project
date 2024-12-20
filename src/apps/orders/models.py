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
    link = models.ForeignKey('links.Link', on_delete=models.SET_NULL, blank=True, null=True)

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
        QAYTIB_KELDI = 6, 'QAYTIB_KELDI'

    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.YANGI)
    admin = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, blank=True, null=True, related_name='admin_orders')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='product_orders')
    operator = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, blank=True, null=True, related_name='operator_orders')

    total_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    estimated_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

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
        if not self.link and not self.product:
            raise ValidationError("product does not exists")

        if self.link:
            self.admin = self.link.user
            self.product = self.link.product

            if not self.id:
                self.estimated_balance = self.product.admin_money * self.product_count

                self.admin.estimated_balance =+ self.product.admin_money * self.product_count

            if self.status == self.StatusChoices.YETKAZIB_BERILDI:
                self.estimated_balance -= self.product.admin_money * self.product_count
                self.total_balance =+ self.product.admin_money * self.product_count

                self.admin.estimated_balance -= self.product.admin_money * self.product_count
                self.admin.total_balance =+ self.product.admin_money * self.product_count
                self.admin.save()

            if self.status == self.StatusChoices.QAYTIB_KELDI:
                self.estimated_balance -= self.product.admin_money * self.product_count

                self.admin.estimated_balance -= self.product.admin_money * self.product_count
                self.admin.save()

        super().save(*args, **kwargs)

    def update(self):
        pass

    def assign_operator(self, user_id):
        if self.operator is not None:
            raise ValidationError("Operator allaqachon tayinlangan.")

        self.operator_id = user_id
        self.save()

    def __str__(self):
        return f"Order {self.id} for {self.buyer_name} from {self.area}"
