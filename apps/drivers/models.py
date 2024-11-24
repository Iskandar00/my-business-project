from django.db import models

from apps.users.models import CustomUser
from apps.orders.models import Order

class ProductDelivery(models.Model):

    class Status(models.IntegerChoices):
        YETKAZILMOQDA = 1, 'YETKAZILMOQDA'
        YETKAZIB_BERILDI = 2, 'YETKAZIB_BERILDI'
        QAYTIB_KELDI = 3, 'QAYTIB_KELDI'


    delivery = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, limit_choices_to={'role': CustomUser.RoleChoices.Supplier}, related_name='deliveries')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True)

    status = models.IntegerField(choices=Status.choices, default=Status.YETKAZILMOQDA)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    product_count = models.PositiveSmallIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.product = self.order.product
        self.product_count = self.order.product_count

        super().save(*args, **kwargs)

        if self.status == self.Status.YETKAZIB_BERILDI:
            self.order.status = Order.StatusChoices.YETKAZIB_BERILDI
            self.order.save()
        elif self.status == self.Status.QAYTIB_KELDI:
            self.order.status = Order.StatusChoices.QAYTIB_KELDI
            self.order.save()

    def __str__(self):
        return self.delivery



